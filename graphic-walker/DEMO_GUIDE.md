# GraphicWalker Demo Guide

This guide walks you through exploring the GraphicWalker interface and creating various visualizations.

## Starting the Application

```bash
cd graphic-walker
npm run dev
```

Open your browser to `http://localhost:5173`

## Understanding the Interface

### Main Areas

1. **Data Panel (Left Sidebar)**
   - Dimensions: Date, Product, Category, Region
   - Measures: Sales, Quantity, Profit

2. **Visualization Canvas (Center)**
   - Where your charts appear
   - Drag and drop to create visualizations

3. **Encoding Shelf (Top)**
   - X-axis, Y-axis
   - Color, Size, Shape
   - Filters

4. **Toolbar (Top Right)**
   - Chart type selector
   - Export options
   - Settings

## Step-by-Step Tutorials

### Tutorial 1: Basic Bar Chart

**Goal**: Create a bar chart showing sales by product

1. Find the "Product" field in the left panel (under Dimensions)
2. Drag "Product" to the X-axis area at the top
3. Find "Sales" in the Measures section
4. Drag "Sales" to the Y-axis area
5. You should see a bar chart appear automatically

**Expected Result**: A bar chart with products on X-axis and sales amounts on Y-axis

### Tutorial 2: Time Series Line Chart

**Goal**: Show sales trends over time

1. Clear the previous chart (click the refresh icon or create a new tab)
2. Drag "Date" to the X-axis
3. Drag "Sales" to the Y-axis
4. Click the chart type dropdown and select "Line"

**Expected Result**: A line chart showing sales over time from January to March 2024

### Tutorial 3: Stacked Bar Chart with Color

**Goal**: Compare sales across regions, colored by category

1. Create a new visualization tab
2. Drag "Region" to the X-axis
3. Drag "Sales" to the Y-axis
4. Drag "Category" to the "Color" encoding
5. The bars should now be stacked and colored by category

**Expected Result**: Stacked bars showing Electronics vs Furniture sales in each region

### Tutorial 4: Scatter Plot

**Goal**: Explore relationship between quantity and profit

1. Create a new tab
2. Drag "Quantity" to the X-axis
3. Drag "Profit" to the Y-axis
4. Select "Point" as the chart type
5. Optional: Drag "Product" to Color to see patterns by product

**Expected Result**: Scatter plot showing profit vs quantity relationship

### Tutorial 5: Using Filters

**Goal**: Focus on specific products or regions

1. Create any visualization (e.g., sales by product)
2. Click the filter icon in the toolbar
3. Select a field to filter (e.g., "Category")
4. Choose "Electronics" or "Furniture"
5. The visualization updates to show only filtered data

**Expected Result**: Chart showing only the selected category

### Tutorial 6: Aggregation Options

**Goal**: Calculate average instead of sum

1. Create a bar chart with Sales
2. Click on the "Sales" pill in the Y-axis area
3. A menu appears with aggregation options
4. Change from "Sum" to "Average"
5. The chart recalculates showing average sales

**Options Available**:
- Sum (default for measures)
- Average
- Count
- Min
- Max
- Median

### Tutorial 7: Multiple Measures

**Goal**: Compare sales and profit side by side

1. Drag "Product" to X-axis
2. Drag "Sales" to Y-axis
3. Drag "Profit" to Y-axis (drop it next to Sales)
4. You now have two measures on the same chart

**Expected Result**: Grouped bar chart comparing sales and profit

### Tutorial 8: Pivot Table View

**Goal**: Create a cross-tabulation

1. Click the chart type selector
2. Choose "Table" view
3. Drag "Region" to Rows
4. Drag "Product" to Columns
5. Drag "Sales" to Values

**Expected Result**: A pivot table showing sales by region and product

## Advanced Techniques

### Creating Multiple Charts

1. Click the "+" button to create a new tab
2. Each tab can have a different visualization
3. All tabs share the same underlying data
4. Use tabs to create a dashboard-like experience

### Sorting Data

1. Click on a dimension pill (e.g., Product on X-axis)
2. Select sorting options:
   - Sort alphabetically (A-Z or Z-A)
   - Sort by measure value (ascending/descending)

### Date Formatting

1. When using the Date field, click on it
2. Choose granularity:
   - Year
   - Month
   - Day
   - Week

### Custom Colors

1. Drag a dimension to the Color encoding
2. Click the color legend
3. Customize colors for each category

## Sample Insights to Discover

Using the sample data, try to answer these questions:

1. **Which product generates the most sales?**
   - Hint: Product bar chart sorted by sales

2. **Which region is most profitable?**
   - Hint: Region on X, Profit on Y

3. **Is there a seasonal trend in sales?**
   - Hint: Date line chart

4. **What's the profit margin by category?**
   - Hint: Calculate profit/sales ratio or compare side by side

5. **Which product-region combination performs best?**
   - Hint: Use Product on X, Color by Region

## Keyboard Shortcuts

- **Ctrl/Cmd + Z**: Undo
- **Ctrl/Cmd + Y**: Redo
- **Delete**: Remove selected field
- **Tab**: Navigate between fields

## Export Options

### Export Chart
1. Click the export button (top right)
2. Choose format:
   - PNG image
   - SVG vector
   - JSON specification

### Export Data
1. Click the data export option
2. Download as CSV or JSON

## Tips & Tricks

### Quick Tip 1: Field Swapping
- Drag a field from X to Y axis (or vice versa) to quickly swap

### Quick Tip 2: Duplicate Visualizations
- Right-click on a tab to duplicate it
- Make variations of the same chart

### Quick Tip 3: Color Palettes
- Try different color schemes for better accessibility
- Consider colorblind-friendly palettes

### Quick Tip 4: Performance
- With large datasets, use filters to focus on relevant data
- Aggregate before visualizing when possible

## Troubleshooting

### Chart Not Appearing
- Ensure you have both a dimension AND a measure
- Check if filters are too restrictive

### Wrong Aggregation
- Click on the measure pill to change aggregation type
- Default is usually Sum

### Date Not Showing Correctly
- Click on Date field and select proper granularity
- Ensure date format is recognized (YYYY-MM-DD)

### Colors Look Wrong
- Check if the right field is in the Color encoding
- Verify the field has the expected values

## Next Steps

1. **Load Your Own Data**
   - Replace sampleData.ts with your dataset
   - Update field definitions accordingly

2. **Customize the Interface**
   - Adjust colors in App.css
   - Modify header text in App.tsx

3. **Add More Features**
   - Implement data loading from API
   - Add authentication
   - Create pre-built dashboard views

## Learning Resources

- **GraphicWalker Docs**: https://github.com/Kanaries/graphic-walker
- **Vega-Lite Grammar**: https://vega.github.io/vega-lite/
- **Data Visualization Principles**: https://clauswilke.com/dataviz/

## Sample Questions for Practice

Try creating these visualizations:

1. A line chart showing profit trends by month
2. A bar chart of average quantity by product
3. A scatter plot of sales vs profit, colored by region
4. A stacked area chart of sales over time by category
5. A heatmap showing sales by product and region

Happy Visualizing!

---

For more information, see README.md and QUICKSTART.md
