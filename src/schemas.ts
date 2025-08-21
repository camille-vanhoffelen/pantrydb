import { z } from "zod";

// Reusable Zod schemas for input validation

export const itemNameSchema = z.string()
	.min(1, "Item name cannot be empty")
	.max(100, "Item name too long (max 100 characters)")
	.regex(/^[a-zA-Z0-9\s\-'&.()]+$/, "Item name contains invalid characters. Use only letters, numbers, spaces, and basic punctuation")
	.describe("Name of the item, in English, and in singular form, e.g 'banana'");

export const quantitySchema = z.number()
	.int("Quantity must be a whole number")
	.positive("Quantity must be positive")
	.max(999999, "Quantity too large (max 999,999)");

export const packageTypeSchema = z.string()
	.max(50, "Package type too long (max 50 characters)")
	.regex(/^[a-zA-Z0-9\s\-]+$/, "Package type contains invalid characters")
	.optional()
	.describe("Type of item package. e.g 'bottle', 'box', 'bag', 'tray'");

export const packageSizeSchema = z.string()
	.max(50, "Package size too long (max 50 characters)")
	.regex(/^[a-zA-Z0-9\s\-.,]+$/, "Package size contains invalid characters")
	.optional()
	.describe("Size of item package. e.g '250 grams', '3 liters'");