import OAuthProvider from "@cloudflare/workers-oauth-provider";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { McpAgent } from "agents/mcp";
import { z } from "zod";
import { GitHubHandler } from "./github-handler";

// Context from the auth process, encrypted & stored in the auth token
// and provided to the DurableMCP as this.props
type Props = {
	login: string;
	name: string;
	email: string;
	accessToken: string;
};

export class MyMCP extends McpAgent<Env, Record<string, never>, Props> {
	server = new McpServer({
		name: "PantryDB MCP Server",
		version: "1.0.0",
	});

	async init() {
		this.server.tool(
			"listPantryItems",
			"List all items in the pantry",
			{},
			async () => {
				const result = await this.env.DB.prepare("SELECT ItemName, ItemAmount FROM PantryItems").all();
				return {
					content: [
						{
							text: JSON.stringify(result.results, null, 2),
							type: "text",
						},
					],
				};
			},
		);

		this.server.tool(
			"addPantryItem",
			"Add an item to the pantry or update amount if it already exists",
			{ 
				name: z.string().describe("Name of the item, in English, and in singular form, e.g 'banana'"),
				amount: z.number().int().positive().describe("Amount to add (must be positive)")
			},
			async ({ name, amount }) => {
				try {
					const existing = await this.env.DB.prepare(
						"SELECT ItemID, ItemAmount FROM PantryItems WHERE ItemName = ?"
					).bind(name.toLowerCase()).first();

					if (existing) {
						const currentAmount = existing.ItemAmount as number;
						const newAmount = currentAmount + amount;
						await this.env.DB.prepare(
							"UPDATE PantryItems SET ItemAmount = ? WHERE ItemID = ?"
						).bind(newAmount, existing.ItemID).run();
						
						return {
							content: [
								{
									text: `Added item, updated amount: ${newAmount}`,
									type: "text",
								},
							],
						};
					} else {
						await this.env.DB.prepare(
							"INSERT INTO PantryItems (ItemName, ItemAmount) VALUES (?, ?)"
						).bind(name.toLowerCase(), amount).run();
						
						return {
							content: [
								{
									text: `Added item, updated amount: ${amount}`,
									type: "text",
								},
							],
						};
					}
				} catch (error) {
					// TODO actually return failure
					return {
						content: [
							{
								text: `Error adding item: ${error}`,
								type: "text",
							},
						],
					};
				}
			},
		);

		this.server.tool(
			"removePantryItem",
			"Remove an item from the pantry or decrease amount if some remains",
			{ 
				name: z.string().describe("Name of the item, in English, and in singular form, e.g 'banana'"),
				amount: z.number().int().positive().describe("Amount to add (must be positive)")
			},
			async ({ name, amount }) => {
				try {
					const existing = await this.env.DB.prepare(
						"SELECT ItemID, ItemAmount FROM PantryItems WHERE ItemName = ?"
					).bind(name.toLowerCase()).first();

					if (!existing) {
						// TODO actually return failure
						return {
							content: [
								{
									text: `Item not found: ${name}`,
									type: "text",
								},
							],
						};
					}

					const currentAmount = existing.ItemAmount as number;
					
					if (currentAmount < amount) {
						return {
						// TODO actually return failure
							content: [
								{
									text: `Insufficient amount: ${name} has ${currentAmount}, requested to remove ${amount}`,
									type: "text",
								},
							],
						};
					}

					const newAmount = currentAmount - amount;

					if (newAmount === 0) {
						await this.env.DB.prepare(
							"DELETE FROM PantryItems WHERE ItemID = ?"
						).bind(existing.ItemID).run();

						return {
							content: [
								{
									text: `Removed item, updated amount: 0`,
									type: "text",
								},
							],
						};
					} else {
						await this.env.DB.prepare(
							"UPDATE PantryItems SET ItemAmount = ? WHERE ItemID = ?"
						).bind(newAmount, existing.ItemID).run();

						return {
							content: [
								{
									text: `Removed item, updated amount: ${newAmount}`,
									type: "text",
								},
							],
						};
					}
				} catch (error) {
					return {
						// TODO actually return failure
						content: [
							{
								text: `Error removing item: ${error}`,
								type: "text",
							},
						],
					};
				}
			},
		);
	}
}

export default new OAuthProvider({
	apiHandler: MyMCP.mount("/sse") as any,
	apiRoute: "/sse",
	authorizeEndpoint: "/authorize",
	clientRegistrationEndpoint: "/register",
	defaultHandler: GitHubHandler as any,
	tokenEndpoint: "/token",
});
