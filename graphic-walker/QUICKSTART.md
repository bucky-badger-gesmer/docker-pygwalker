# Quick Start Guide

Get up and running with GraphicWalker in 5 minutes.

## Installation

```bash
cd graphic-walker
npm install
npm run dev
```

That's it! Open your browser to `http://localhost:5173`

## What You'll See

The demo application loads with:
- Sample sales data (30 records)
- Multiple dimensions (Date, Product, Category, Region)
- Multiple measures (Sales, Quantity, Profit)

## Try These Visualizations

### 1. Sales by Product (Bar Chart)
- Drag "Product" to the X-axis
- Drag "Sales" to the Y-axis
- Automatic bar chart created

### 2. Sales Over Time (Line Chart)
- Drag "Date" to the X-axis
- Drag "Sales" to the Y-axis
- Change chart type to "Line"

### 3. Regional Sales Comparison
- Drag "Region" to the X-axis
- Drag "Sales" to the Y-axis
- Drag "Category" to Color
- Stacked bar chart created

### 4. Profit Analysis
- Drag "Product" to Rows
- Drag "Profit" to the measure area
- Add "Region" as a filter

## Key Features to Explore

1. **Drag and Drop**: Move fields between different areas (X, Y, Color, Size, etc.)
2. **Filters**: Click the filter icon to add data filters
3. **Aggregations**: Click on measures to change aggregation (Sum, Avg, Count, etc.)
4. **Chart Types**: Switch between bar, line, area, scatter, and more
5. **Multiple Views**: Create multiple charts in tabs

## Next Steps

1. Replace sample data with your own dataset in `src/data/sampleData.ts`
2. Update field definitions in `src/components/GraphicWalkerDemo.tsx`
3. Customize styling in `src/App.css`

## Common Issues

**Port already in use?**
```bash
npm run dev -- --port 3000
```

**Build errors?**
```bash
rm -rf node_modules package-lock.json
npm install
```

**TypeScript errors?**
Check that your data matches the field definitions in `GraphicWalkerDemo.tsx`

## Learn More

See the full [README.md](./README.md) for detailed documentation.
