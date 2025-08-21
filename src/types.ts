// Database result types for PantryDB

export interface PantryItem {
	ItemID: number;
	ItemName: string;
	ItemQuantity: number;
	PackageType: string | null;
	PackageSize: string | null;
}

export interface PantryItemPartial {
	ItemID: number;
	ItemQuantity: number;
}