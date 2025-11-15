export interface SalesRecord {
  date: string;
  product: string;
  category: string;
  region: string;
  sales: number;
  quantity: number;
  profit: number;
}

export const sampleData: SalesRecord[] = [
  { date: "2024-01-15", product: "Laptop", category: "Electronics", region: "North", sales: 1200, quantity: 10, profit: 240 },
  { date: "2024-01-16", product: "Mouse", category: "Electronics", region: "South", sales: 300, quantity: 50, profit: 90 },
  { date: "2024-01-17", product: "Keyboard", category: "Electronics", region: "East", sales: 450, quantity: 30, profit: 135 },
  { date: "2024-01-18", product: "Monitor", category: "Electronics", region: "West", sales: 900, quantity: 15, profit: 180 },
  { date: "2024-01-19", product: "Laptop", category: "Electronics", region: "South", sales: 2400, quantity: 20, profit: 480 },
  { date: "2024-01-20", product: "Desk", category: "Furniture", region: "North", sales: 600, quantity: 8, profit: 120 },
  { date: "2024-01-21", product: "Chair", category: "Furniture", region: "East", sales: 800, quantity: 20, profit: 200 },
  { date: "2024-01-22", product: "Mouse", category: "Electronics", region: "West", sales: 360, quantity: 60, profit: 108 },
  { date: "2024-01-23", product: "Desk Lamp", category: "Furniture", region: "North", sales: 200, quantity: 25, profit: 50 },
  { date: "2024-01-24", product: "Laptop", category: "Electronics", region: "East", sales: 3600, quantity: 30, profit: 720 },
  { date: "2024-02-01", product: "Monitor", category: "Electronics", region: "South", sales: 1800, quantity: 30, profit: 360 },
  { date: "2024-02-02", product: "Keyboard", category: "Electronics", region: "North", sales: 525, quantity: 35, profit: 157.5 },
  { date: "2024-02-03", product: "Chair", category: "Furniture", region: "West", sales: 1000, quantity: 25, profit: 250 },
  { date: "2024-02-04", product: "Desk", category: "Furniture", region: "South", sales: 750, quantity: 10, profit: 150 },
  { date: "2024-02-05", product: "Mouse", category: "Electronics", region: "East", sales: 420, quantity: 70, profit: 126 },
  { date: "2024-02-06", product: "Laptop", category: "Electronics", region: "West", sales: 2640, quantity: 22, profit: 528 },
  { date: "2024-02-07", product: "Desk Lamp", category: "Furniture", region: "South", sales: 240, quantity: 30, profit: 60 },
  { date: "2024-02-08", product: "Monitor", category: "Electronics", region: "North", sales: 1080, quantity: 18, profit: 216 },
  { date: "2024-02-09", product: "Keyboard", category: "Electronics", region: "East", sales: 495, quantity: 33, profit: 148.5 },
  { date: "2024-02-10", product: "Chair", category: "Furniture", region: "West", sales: 880, quantity: 22, profit: 220 },
  { date: "2024-03-01", product: "Laptop", category: "Electronics", region: "North", sales: 2880, quantity: 24, profit: 576 },
  { date: "2024-03-02", product: "Mouse", category: "Electronics", region: "South", sales: 390, quantity: 65, profit: 117 },
  { date: "2024-03-03", product: "Desk", category: "Furniture", region: "East", sales: 675, quantity: 9, profit: 135 },
  { date: "2024-03-04", product: "Monitor", category: "Electronics", region: "West", sales: 1620, quantity: 27, profit: 324 },
  { date: "2024-03-05", product: "Keyboard", category: "Electronics", region: "North", sales: 510, quantity: 34, profit: 153 },
  { date: "2024-03-06", product: "Chair", category: "Furniture", region: "South", sales: 960, quantity: 24, profit: 240 },
  { date: "2024-03-07", product: "Desk Lamp", category: "Furniture", region: "East", sales: 280, quantity: 35, profit: 70 },
  { date: "2024-03-08", product: "Laptop", category: "Electronics", region: "West", sales: 3120, quantity: 26, profit: 624 },
  { date: "2024-03-09", product: "Mouse", category: "Electronics", region: "North", sales: 330, quantity: 55, profit: 99 },
  { date: "2024-03-10", product: "Monitor", category: "Electronics", region: "South", sales: 1440, quantity: 24, profit: 288 },
];
