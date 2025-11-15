# Code Examples

Advanced examples for integrating and customizing GraphicWalker in your React application.

## Table of Contents

1. [Loading Data from CSV](#loading-data-from-csv)
2. [Loading Data from API](#loading-data-from-api)
3. [Custom Field Definitions](#custom-field-definitions)
4. [Multiple Datasets](#multiple-datasets)
5. [Theming and Styling](#theming-and-styling)
6. [Export Functionality](#export-functionality)
7. [State Management](#state-management)
8. [Performance Optimization](#performance-optimization)

## Loading Data from CSV

```typescript
// src/utils/csvLoader.ts
import { IRow } from '@kanaries/graphic-walker/interfaces';

export async function loadCSV(file: File): Promise<IRow[]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      const text = e.target?.result as string;
      const rows = text.split('\n');
      const headers = rows[0].split(',');

      const data: IRow[] = rows.slice(1)
        .filter(row => row.trim())
        .map(row => {
          const values = row.split(',');
          const obj: IRow = {};
          headers.forEach((header, index) => {
            obj[header.trim()] = values[index]?.trim();
          });
          return obj;
        });

      resolve(data);
    };

    reader.onerror = reject;
    reader.readAsText(file);
  });
}

// Usage in component
import { useState } from 'react';
import { loadCSV } from '../utils/csvLoader';

const CSVUploader: React.FC = () => {
  const [data, setData] = useState<IRow[]>([]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const csvData = await loadCSV(file);
      setData(csvData);
    }
  };

  return (
    <div>
      <input type="file" accept=".csv" onChange={handleFileUpload} />
      {data.length > 0 && <GraphicWalker data={data} fields={fields} />}
    </div>
  );
};
```

## Loading Data from API

```typescript
// src/hooks/useDataFetch.ts
import { useState, useEffect } from 'react';
import type { IRow } from '@kanaries/graphic-walker/interfaces';

export function useDataFetch(url: string) {
  const [data, setData] = useState<IRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const jsonData = await response.json();
        setData(jsonData);
      } catch (e) {
        setError(e as Error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [url]);

  return { data, loading, error };
}

// Usage in component
const APIDataViewer: React.FC = () => {
  const { data, loading, error } = useDataFetch('https://api.example.com/data');

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <GraphicWalker data={data} fields={inferFields(data)} />;
};
```

## Custom Field Definitions

```typescript
// src/utils/fieldInference.ts
import type { IRow, IField } from '@kanaries/graphic-walker/interfaces';

export function inferFields(data: IRow[]): IField[] {
  if (data.length === 0) return [];

  const sample = data[0];
  return Object.keys(sample).map(key => {
    const value = sample[key];
    const field: IField = {
      fid: key,
      name: key.charAt(0).toUpperCase() + key.slice(1),
      semanticType: inferSemanticType(value, data, key),
      analyticType: inferAnalyticType(value),
    };
    return field;
  });
}

function inferSemanticType(
  value: any,
  data: IRow[],
  key: string
): 'temporal' | 'nominal' | 'quantitative' | 'ordinal' {
  // Check if it's a date
  if (key.toLowerCase().includes('date') ||
      key.toLowerCase().includes('time')) {
    return 'temporal';
  }

  // Check if numeric
  if (typeof value === 'number') {
    return 'quantitative';
  }

  // Check for numeric strings
  if (typeof value === 'string' && !isNaN(Number(value))) {
    return 'quantitative';
  }

  // Check if ordinal (small set of ordered values)
  const unique = new Set(data.map(row => row[key]));
  if (unique.size < 10 &&
      ['low', 'medium', 'high'].some(v =>
        Array.from(unique).some(u =>
          String(u).toLowerCase().includes(v)
        )
      )) {
    return 'ordinal';
  }

  // Default to nominal
  return 'nominal';
}

function inferAnalyticType(
  value: any
): 'dimension' | 'measure' {
  return typeof value === 'number' ||
         (typeof value === 'string' && !isNaN(Number(value)))
    ? 'measure'
    : 'dimension';
}
```

## Multiple Datasets

```typescript
// src/components/MultiDatasetViewer.tsx
import { useState } from 'react';
import { GraphicWalker } from '@kanaries/graphic-walker';

interface Dataset {
  name: string;
  data: IRow[];
  fields: IField[];
}

const MultiDatasetViewer: React.FC = () => {
  const [datasets] = useState<Dataset[]>([
    {
      name: 'Sales Data',
      data: salesData,
      fields: salesFields,
    },
    {
      name: 'Customer Data',
      data: customerData,
      fields: customerFields,
    },
  ]);

  const [activeDataset, setActiveDataset] = useState(0);

  return (
    <div>
      <select
        value={activeDataset}
        onChange={(e) => setActiveDataset(Number(e.target.value))}
      >
        {datasets.map((ds, idx) => (
          <option key={idx} value={idx}>
            {ds.name}
          </option>
        ))}
      </select>

      <GraphicWalker
        data={datasets[activeDataset].data}
        fields={datasets[activeDataset].fields}
      />
    </div>
  );
};
```

## Theming and Styling

```typescript
// src/components/ThemedGraphicWalker.tsx
import { GraphicWalker } from '@kanaries/graphic-walker';
import { useState, useEffect } from 'react';

const ThemedGraphicWalker: React.FC<GraphicWalkerProps> = (props) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  // Detect system theme
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    setTheme(mediaQuery.matches ? 'dark' : 'light');

    const handler = (e: MediaQueryListEvent) => {
      setTheme(e.matches ? 'dark' : 'light');
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return (
    <div className={`gw-container ${theme}`}>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </button>
      <GraphicWalker
        {...props}
        dark={theme}
      />
    </div>
  );
};

// Add to your CSS
const styles = `
.gw-container.dark {
  background-color: #1a1a1a;
  color: #ffffff;
}

.gw-container.light {
  background-color: #ffffff;
  color: #000000;
}
`;
```

## Export Functionality

```typescript
// src/hooks/useGraphicWalkerExport.ts
import { useRef, useCallback } from 'react';

export function useGraphicWalkerExport() {
  const exportData = useCallback((data: IRow[], filename: string) => {
    const csv = convertToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  }, []);

  const exportJSON = useCallback((data: IRow[], filename: string) => {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }, []);

  return { exportData, exportJSON };
}

function convertToCSV(data: IRow[]): string {
  if (data.length === 0) return '';

  const headers = Object.keys(data[0]);
  const headerRow = headers.join(',');

  const rows = data.map(row =>
    headers.map(header => {
      const value = row[header];
      return typeof value === 'string' && value.includes(',')
        ? `"${value}"`
        : value;
    }).join(',')
  );

  return [headerRow, ...rows].join('\n');
}

// Usage
const GraphicWalkerWithExport: React.FC = () => {
  const { exportData, exportJSON } = useGraphicWalkerExport();

  return (
    <div>
      <button onClick={() => exportData(data, 'visualization-data')}>
        Export CSV
      </button>
      <button onClick={() => exportJSON(data, 'visualization-data')}>
        Export JSON
      </button>
      <GraphicWalker data={data} fields={fields} />
    </div>
  );
};
```

## State Management

```typescript
// src/contexts/DataContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react';
import type { IRow, IField } from '@kanaries/graphic-walker/interfaces';

interface DataContextType {
  data: IRow[];
  fields: IField[];
  setData: (data: IRow[]) => void;
  setFields: (fields: IField[]) => void;
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export function DataProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<IRow[]>([]);
  const [fields, setFields] = useState<IField[]>([]);

  return (
    <DataContext.Provider value={{ data, fields, setData, setFields }}>
      {children}
    </DataContext.Provider>
  );
}

export function useData() {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useData must be used within DataProvider');
  }
  return context;
}

// Usage in App
import { DataProvider } from './contexts/DataContext';

function App() {
  return (
    <DataProvider>
      <YourComponents />
    </DataProvider>
  );
}

// Usage in component
import { useData } from '../contexts/DataContext';

const DataViewer: React.FC = () => {
  const { data, fields } = useData();
  return <GraphicWalker data={data} fields={fields} />;
};
```

## Performance Optimization

```typescript
// src/components/OptimizedGraphicWalker.tsx
import { memo, useMemo, useCallback } from 'react';
import { GraphicWalker } from '@kanaries/graphic-walker';

interface Props {
  rawData: IRow[];
  rawFields: IField[];
}

const OptimizedGraphicWalker = memo<Props>(({ rawData, rawFields }) => {
  // Memoize data to prevent unnecessary recalculations
  const data = useMemo(() => {
    // Apply any transformations
    return rawData.map(row => ({
      ...row,
      // Add computed fields if needed
    }));
  }, [rawData]);

  // Memoize fields
  const fields = useMemo(() => {
    return rawFields.map(field => ({
      ...field,
      // Apply any field transformations
    }));
  }, [rawFields]);

  // Memoize callback handlers
  const handleVisualizationChange = useCallback((viz: any) => {
    console.log('Visualization changed:', viz);
  }, []);

  return (
    <GraphicWalker
      data={data}
      fields={fields}
    />
  );
}, (prevProps, nextProps) => {
  // Custom comparison for memo
  return (
    prevProps.rawData.length === nextProps.rawData.length &&
    prevProps.rawFields.length === nextProps.rawFields.length
  );
});

export default OptimizedGraphicWalker;
```

## Data Filtering

```typescript
// src/hooks/useDataFilter.ts
import { useState, useMemo } from 'react';
import type { IRow } from '@kanaries/graphic-walker/interfaces';

export function useDataFilter(data: IRow[]) {
  const [filters, setFilters] = useState<Record<string, any>>({});

  const filteredData = useMemo(() => {
    return data.filter(row => {
      return Object.entries(filters).every(([key, value]) => {
        if (value === null || value === undefined) return true;
        if (Array.isArray(value)) {
          return value.includes(row[key]);
        }
        return row[key] === value;
      });
    });
  }, [data, filters]);

  const addFilter = (key: string, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const removeFilter = (key: string) => {
    setFilters(prev => {
      const next = { ...prev };
      delete next[key];
      return next;
    });
  };

  const clearFilters = () => {
    setFilters({});
  };

  return {
    filteredData,
    filters,
    addFilter,
    removeFilter,
    clearFilters,
  };
}

// Usage
const FilterableViewer: React.FC = () => {
  const { filteredData, addFilter, clearFilters } = useDataFilter(rawData);

  return (
    <div>
      <button onClick={() => addFilter('category', 'Electronics')}>
        Show Electronics Only
      </button>
      <button onClick={clearFilters}>Clear Filters</button>
      <GraphicWalker data={filteredData} fields={fields} />
    </div>
  );
};
```

## Data Aggregation

```typescript
// src/utils/dataAggregation.ts
import type { IRow } from '@kanaries/graphic-walker/interfaces';

export function aggregateData(
  data: IRow[],
  groupBy: string,
  aggregations: Record<string, 'sum' | 'avg' | 'count' | 'min' | 'max'>
): IRow[] {
  const groups = new Map<string, IRow[]>();

  // Group data
  data.forEach(row => {
    const key = row[groupBy];
    if (!groups.has(key)) {
      groups.set(key, []);
    }
    groups.get(key)!.push(row);
  });

  // Aggregate
  return Array.from(groups.entries()).map(([key, rows]) => {
    const result: IRow = { [groupBy]: key };

    Object.entries(aggregations).forEach(([field, method]) => {
      const values = rows.map(row => Number(row[field])).filter(v => !isNaN(v));

      switch (method) {
        case 'sum':
          result[field] = values.reduce((a, b) => a + b, 0);
          break;
        case 'avg':
          result[field] = values.reduce((a, b) => a + b, 0) / values.length;
          break;
        case 'count':
          result[field] = values.length;
          break;
        case 'min':
          result[field] = Math.min(...values);
          break;
        case 'max':
          result[field] = Math.max(...values);
          break;
      }
    });

    return result;
  });
}

// Usage
const aggregated = aggregateData(
  data,
  'region',
  { sales: 'sum', quantity: 'sum', profit: 'avg' }
);
```

## Best Practices

### 1. Data Preparation
```typescript
// Clean and validate data before passing to GraphicWalker
function prepareData(rawData: any[]): IRow[] {
  return rawData
    .filter(row => row !== null && row !== undefined)
    .map(row => ({
      ...row,
      // Convert dates to ISO format
      date: row.date instanceof Date
        ? row.date.toISOString()
        : row.date,
      // Ensure numbers are numbers
      sales: Number(row.sales) || 0,
    }));
}
```

### 2. Error Boundaries
```typescript
// Wrap GraphicWalker in error boundary
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error }: { error: Error }) {
  return (
    <div role="alert">
      <p>Something went wrong:</p>
      <pre>{error.message}</pre>
    </div>
  );
}

<ErrorBoundary FallbackComponent={ErrorFallback}>
  <GraphicWalker data={data} fields={fields} />
</ErrorBoundary>
```

### 3. Loading States
```typescript
function DataVisualization() {
  const [isLoading, setIsLoading] = useState(true);

  if (isLoading) {
    return (
      <div className="loading-container">
        <Spinner />
        <p>Loading data...</p>
      </div>
    );
  }

  return <GraphicWalker data={data} fields={fields} />;
}
```

---

For more examples and documentation, visit the [GraphicWalker GitHub repository](https://github.com/Kanaries/graphic-walker).
