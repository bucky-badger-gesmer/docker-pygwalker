# GraphicWalker Demo

A modern React + TypeScript application demonstrating the integration of [@kanaries/graphic-walker](https://github.com/Kanaries/graphic-walker) for interactive data visualization.

## Overview

This project showcases how to integrate GraphicWalker into a React application using Vite as the build tool. GraphicWalker is a powerful visualization library that provides a Tableau-like interface for exploring and analyzing data directly in the browser.

## Features

- Built with Vite for fast development and optimized builds
- TypeScript for type safety
- GraphicWalker integration with sample sales data
- Interactive data exploration with drag-and-drop interface
- Support for multiple chart types (bar, line, area, scatter, etc.)
- Responsive design

## Prerequisites

- Node.js 16 or higher
- npm or yarn package manager

## Installation

1. Navigate to the project directory:
```bash
cd graphic-walker
```

2. Install dependencies:
```bash
npm install
```

Note: This project uses `--legacy-peer-deps` due to React version compatibility. The GraphicWalker library officially supports React 17-18, while Vite's latest template uses React 19. The application works correctly despite the peer dependency warning.

## Running the Application

### Development Mode

Start the development server:
```bash
npm run dev
```

The application will open at `http://localhost:5173` (or another port if 5173 is in use).

### Production Build

Build the application for production:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
graphic-walker/
├── src/
│   ├── components/
│   │   └── GraphicWalkerDemo.tsx    # Main GraphicWalker component
│   ├── data/
│   │   └── sampleData.ts            # Sample dataset
│   ├── App.tsx                      # Root component
│   ├── App.css                      # App styles
│   ├── index.css                    # Global styles
│   └── main.tsx                     # Entry point
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## Using GraphicWalker

### Basic Integration

The GraphicWalker component requires two main props:

1. **data**: An array of objects representing your dataset
2. **fields**: Metadata describing each field in your data

```tsx
import { GraphicWalker } from '@kanaries/graphic-walker';
import type { IRow } from '@kanaries/graphic-walker/interfaces';

const MyComponent = () => {
  const data: IRow[] = [
    { date: "2024-01-15", product: "Laptop", sales: 1200 },
    // ... more data
  ];

  const fields = [
    {
      fid: 'date',
      name: 'Date',
      semanticType: 'temporal',
      analyticType: 'dimension',
    },
    {
      fid: 'sales',
      name: 'Sales',
      semanticType: 'quantitative',
      analyticType: 'measure',
    },
  ];

  return (
    <GraphicWalker
      data={data}
      fields={fields}
      i18nLang="en-US"
    />
  );
};
```

### Field Types

**Semantic Types:**
- `temporal`: Date/time values
- `nominal`: Categorical values (text)
- `ordinal`: Ordered categorical values
- `quantitative`: Numeric values

**Analytic Types:**
- `dimension`: Categories for grouping data
- `measure`: Numeric values for aggregation

## Sample Data

The project includes sample sales data with the following fields:
- Date (temporal dimension)
- Product (nominal dimension)
- Category (nominal dimension)
- Region (nominal dimension)
- Sales (quantitative measure)
- Quantity (quantitative measure)
- Profit (quantitative measure)

## Customization

### Adding Your Own Data

1. Create a new data file in `src/data/`:
```typescript
export const myData = [
  { field1: value1, field2: value2, ... },
  // ... more records
];
```

2. Update `GraphicWalkerDemo.tsx` to use your data:
```typescript
import { myData } from '../data/myData';
```

3. Define appropriate fields metadata matching your data structure.

### Styling

The application uses CSS for styling. Key files:
- `src/index.css`: Global styles
- `src/App.css`: App layout styles
- Inline styles in components for specific adjustments

## Known Issues

- React 19 peer dependency warning (can be safely ignored)
- Some npm audit warnings from GraphicWalker dependencies (low severity)

## Technologies

- **React 19**: Modern React with concurrent features
- **TypeScript 5.9**: Type-safe development
- **Vite 7**: Next-generation frontend tooling
- **GraphicWalker 0.4.77**: Interactive data visualization
- **ESLint**: Code quality and consistency

## Performance

The application is optimized for performance:
- Vite's fast HMR (Hot Module Replacement)
- Efficient bundle splitting
- Optimized production builds
- Lazy loading support

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Contributing

To contribute to this project:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## Resources

- [GraphicWalker Documentation](https://github.com/Kanaries/graphic-walker)
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
- GraphicWalker: [GitHub Issues](https://github.com/Kanaries/graphic-walker/issues)
- React: [React Community](https://react.dev/community)
- Vite: [Vite Discord](https://chat.vitejs.dev/)
