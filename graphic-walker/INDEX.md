# GraphicWalker Demo - Documentation Index

Welcome to the GraphicWalker Demo project! This document helps you navigate all available documentation.

## Quick Links

- **New User?** Start with [QUICKSTART.md](./QUICKSTART.md) (5 minutes)
- **Want to explore?** Check [DEMO_GUIDE.md](./DEMO_GUIDE.md)
- **Need code examples?** See [CODE_EXAMPLES.md](./CODE_EXAMPLES.md)
- **Want full details?** Read [README.md](./README.md)
- **Project overview?** View [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)

## Documentation Files

### 1. QUICKSTART.md (1.8 KB)
**5-minute getting started guide**

- Installation steps
- What you'll see
- Try these visualizations
- Common issues
- Next steps

**Best for**: Getting up and running immediately

### 2. README.md (5.4 KB)
**Comprehensive project documentation**

- Project overview and features
- Installation and setup
- Project structure
- Using GraphicWalker
- Field types and configuration
- Customization guide
- Technologies used
- Resources and support

**Best for**: Understanding the full project

### 3. DEMO_GUIDE.md (7.0 KB)
**Step-by-step tutorial guide**

- Interface overview
- 8 detailed tutorials:
  - Basic bar charts
  - Time series
  - Stacked charts
  - Scatter plots
  - Filters
  - Aggregations
  - Multiple measures
  - Pivot tables
- Advanced techniques
- Sample insights to discover
- Keyboard shortcuts
- Export options
- Tips and tricks
- Troubleshooting

**Best for**: Learning how to use GraphicWalker

### 4. CODE_EXAMPLES.md (15 KB)
**Advanced coding examples**

Topics covered:
- Loading data from CSV
- Loading data from API
- Custom field inference
- Multiple datasets
- Theming and styling
- Export functionality
- State management with Context
- Performance optimization
- Data filtering
- Data aggregation
- Error boundaries
- Loading states
- Best practices

**Best for**: Developers implementing custom features

### 5. PROJECT_SUMMARY.md (7.6 KB)
**Technical project overview**

Contents:
- What was built
- Complete project structure
- Technologies used
- Data structure details
- Build results and metrics
- Features implemented
- Known considerations
- Performance metrics
- Next steps
- API reference
- Testing status
- Command reference

**Best for**: Technical understanding and reference

## Suggested Learning Path

### Path 1: Quick Start (Beginner)
1. Read QUICKSTART.md
2. Run the application
3. Follow DEMO_GUIDE.md tutorials
4. Experiment with creating charts

**Time**: 30 minutes

### Path 2: Developer Integration (Intermediate)
1. Read QUICKSTART.md
2. Review README.md
3. Study CODE_EXAMPLES.md
4. Implement custom features
5. Reference PROJECT_SUMMARY.md as needed

**Time**: 2-3 hours

### Path 3: Full Deep Dive (Advanced)
1. Read all documentation in order
2. Explore the codebase
3. Implement advanced examples
4. Optimize and customize
5. Deploy to production

**Time**: 1-2 days

## File Locations

### Source Code
```
src/
├── components/
│   └── GraphicWalkerDemo.tsx    # Main component
├── data/
│   └── sampleData.ts            # Sample dataset
├── types/
│   └── graphic-walker.d.ts      # Type definitions
├── App.tsx                      # Root component
├── App.css                      # Styles
├── index.css                    # Global styles
└── main.tsx                     # Entry point
```

### Documentation
```
.
├── INDEX.md              # This file
├── QUICKSTART.md        # Quick start guide
├── README.md            # Main documentation
├── DEMO_GUIDE.md        # Tutorial guide
├── CODE_EXAMPLES.md     # Code examples
└── PROJECT_SUMMARY.md   # Technical overview
```

### Configuration
```
.
├── package.json         # Dependencies
├── tsconfig.json        # TypeScript config
├── vite.config.ts       # Vite config
└── .gitignore          # Git ignore rules
```

## Key Concepts

### Data Structure
- **IRow**: Single data record (object with key-value pairs)
- **IField**: Field metadata (name, type, semantic info)
- **Dimensions**: Categories for grouping (Product, Region, etc.)
- **Measures**: Numeric values for aggregation (Sales, Profit, etc.)

### Semantic Types
- **temporal**: Dates and times
- **nominal**: Categories (no order)
- **ordinal**: Ordered categories
- **quantitative**: Numbers

### Analytic Types
- **dimension**: Grouping field
- **measure**: Aggregatable numeric field

## Common Tasks

### How do I...

**...start the application?**
```bash
cd graphic-walker
npm install
npm run dev
```
See: QUICKSTART.md

**...create a bar chart?**
Drag a dimension to X-axis, measure to Y-axis
See: DEMO_GUIDE.md, Tutorial 1

**...load my own data?**
Replace data in `src/data/sampleData.ts`
See: CODE_EXAMPLES.md, "Loading Data from CSV"

**...change colors or styling?**
Edit `src/App.css` or use dark mode
See: CODE_EXAMPLES.md, "Theming and Styling"

**...export visualizations?**
Click export button in toolbar
See: DEMO_GUIDE.md, "Export Options"

**...handle API data?**
Use fetch/axios in useEffect
See: CODE_EXAMPLES.md, "Loading Data from API"

**...optimize performance?**
Use useMemo, React.memo, and pagination
See: CODE_EXAMPLES.md, "Performance Optimization"

**...add multiple datasets?**
Use state management and dropdown selector
See: CODE_EXAMPLES.md, "Multiple Datasets"

## Project Statistics

- **Source files**: 6 TypeScript/TSX files
- **Lines of code**: 182 lines
- **Documentation**: 5 markdown files (36.8 KB)
- **Dependencies**: 779 npm packages
- **Build size**: 4.2 MB (1.2 MB gzipped)
- **Build time**: ~8 seconds

## Getting Help

### In this project:
1. Check the relevant documentation file
2. Search CODE_EXAMPLES.md for similar code
3. Review DEMO_GUIDE.md for UI instructions

### External resources:
- GraphicWalker: https://github.com/Kanaries/graphic-walker
- React: https://react.dev
- Vite: https://vitejs.dev
- TypeScript: https://typescriptlang.org

## Contributing

To improve this documentation:
1. Identify what's missing or unclear
2. Add new examples to CODE_EXAMPLES.md
3. Update tutorials in DEMO_GUIDE.md
4. Keep INDEX.md (this file) updated

## Version Information

- **Project**: graphic-walker demo
- **GraphicWalker**: 0.4.77
- **React**: 19.2.0
- **TypeScript**: 5.9.3
- **Vite**: 7.2.2
- **Created**: November 15, 2025

## License

This project is open source and available under the MIT License.

---

**Ready to start?** Head to [QUICKSTART.md](./QUICKSTART.md)!

For questions or issues, refer to the README.md support section.
