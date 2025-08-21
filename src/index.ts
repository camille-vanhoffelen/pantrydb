import OAuthProvider from "@cloudflare/workers-oauth-provider";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { McpAgent } from "agents/mcp";
import { McpError, ErrorCode } from "@modelcontextprotocol/sdk/types.js";
import { GitHubHandler } from "./github-handler";
import { PantryItem, PantryItemPartial } from "./types";
import { itemNameSchema, quantitySchema, packageTypeSchema, packageSizeSchema } from "./schemas";

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
				const result = await this.env.DB.prepare("SELECT ItemName, ItemQuantity, PackageType, PackageSize FROM PantryItems").all<PantryItem>();
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
			"Add an item to the pantry or update quantity if it already exists. Always list pantry items prior to adding new ones in order to reuse correct names, package types, and package sizes if items already exist.",
			{ 
				name: itemNameSchema,
				quantity: quantitySchema.describe("Quantity to add (must be positive)"),
				packageType: packageTypeSchema,
				packageSize: packageSizeSchema,
			},
			async ({ name, quantity, packageType, packageSize}: {
				name: string;
				quantity: number;
				packageType?: string;
				packageSize?: string;
			}) => {
				try {
					const existing = await this.env.DB.prepare(
						"SELECT ItemID, ItemQuantity FROM PantryItems WHERE ItemName = ? AND PackageType IS ? AND PackageSize IS ?"
					).bind(name.toLowerCase(), packageType || null, packageSize || null).first<PantryItemPartial>();

					if (existing) {
						const currentQuantity: number = existing.ItemQuantity;
						const newQuantity: number = currentQuantity + quantity;
						await this.env.DB.prepare(
							"UPDATE PantryItems SET ItemQuantity = ? WHERE ItemID = ?"
						).bind(newQuantity, existing.ItemID).run();
						
						return {
							content: [
								{
									text: `Added item, updated quantity: ${newQuantity}`,
									type: "text",
								},
							],
						};
					} else {
						await this.env.DB.prepare(
							"INSERT INTO PantryItems (ItemName, ItemQuantity, PackageType, PackageSize) VALUES (?, ?, ?, ?)"
						).bind(name.toLowerCase(), quantity, packageType || null, packageSize || null).run();
						
						return {
							content: [
								{
									text: `Added item, updated quantity: ${quantity}`,
									type: "text",
								},
							],
						};
					}
				} catch (error) {
					throw new McpError(ErrorCode.InternalError, `Failed to add item: ${error instanceof Error ? error.message : String(error)}`);
				}
			},
		);

		this.server.tool(
			"removePantryItem",
			"Remove an item from the pantry or decrease quantity if some remains. Always list pantry items prior to removing them in order to use correct names, package types, and package sizes.",
			{ 
				name: itemNameSchema,
				quantity: quantitySchema.describe("Quantity to remove (must be positive)"),
				packageType: packageTypeSchema,
				packageSize: packageSizeSchema,
			},
			async ({ name, quantity, packageType, packageSize }: {
				name: string;
				quantity: number;
				packageType?: string;
				packageSize?: string;
			}) => {
				try {
					const existing = await this.env.DB.prepare(
						"SELECT ItemID, ItemQuantity FROM PantryItems WHERE ItemName = ? AND PackageType IS ? AND PackageSize IS ?"
					).bind(name.toLowerCase(), packageType || null, packageSize || null).first<PantryItemPartial>();

					if (!existing) {
						throw new McpError(ErrorCode.InvalidParams, `Item not found: ${name}`);
					}

					const currentQuantity: number = existing.ItemQuantity;
					
					if (currentQuantity < quantity) {
						throw new McpError(ErrorCode.InvalidParams, `Insufficient quantity: ${name} has ${currentQuantity}, requested to remove ${quantity}`);
					}

					const newQuantity: number = currentQuantity - quantity;

					if (newQuantity === 0) {
						await this.env.DB.prepare(
							"DELETE FROM PantryItems WHERE ItemID = ?"
						).bind(existing.ItemID).run();

						return {
							content: [
								{
									text: `Removed item, updated quantity: 0`,
									type: "text",
								},
							],
						};
					} else {
						await this.env.DB.prepare(
							"UPDATE PantryItems SET ItemQuantity = ? WHERE ItemID = ?"
						).bind(newQuantity, existing.ItemID).run();

						return {
							content: [
								{
									text: `Removed item, updated quantity: ${newQuantity}`,
									type: "text",
								},
							],
						};
					}
				} catch (error) {
					throw new McpError(ErrorCode.InternalError, `Failed to remove item: ${error instanceof Error ? error.message : String(error)}`);
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
