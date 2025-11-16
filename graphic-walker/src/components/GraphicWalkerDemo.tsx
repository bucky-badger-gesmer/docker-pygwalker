import { useState } from 'react';
import { GraphicWalker } from '@kanaries/graphic-walker';
import type { IRow } from '@kanaries/graphic-walker/interfaces';
import { sampleData } from '../data/sampleData';
import FileSelector from './FileSelector';
import { parseDataFile, detectFieldType } from '../utils/fileParser';

interface Field {
  fid: string;
  name: string;
  semanticType: 'nominal' | 'ordinal' | 'quantitative' | 'temporal';
  analyticType: 'dimension' | 'measure';
}

const GraphicWalkerDemo: React.FC = () => {
  // State for data and metadata
  const [data, setData] = useState<IRow[]>(() =>
    sampleData.map((record) => ({
      date: record.date,
      product: record.product,
      category: record.category,
      region: record.region,
      sales: record.sales,
      quantity: record.quantity,
      profit: record.profit,
    }))
  );

  const [fields, setFields] = useState<Field[]>([
    { fid: 'date', name: 'Date', semanticType: 'temporal', analyticType: 'dimension' },
    { fid: 'product', name: 'Product', semanticType: 'nominal', analyticType: 'dimension' },
    { fid: 'category', name: 'Category', semanticType: 'nominal', analyticType: 'dimension' },
    { fid: 'region', name: 'Region', semanticType: 'nominal', analyticType: 'dimension' },
    { fid: 'sales', name: 'Sales', semanticType: 'quantitative', analyticType: 'measure' },
    { fid: 'quantity', name: 'Quantity', semanticType: 'quantitative', analyticType: 'measure' },
    { fid: 'profit', name: 'Profit', semanticType: 'quantitative', analyticType: 'measure' },
  ]);

  const [fileName, setFileName] = useState('sample_data.csv');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Handle file selection and parsing
  const handleFileSelected = async (file: File) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await parseDataFile(file);

      if (!result.success || !result.data) {
        setError(result.error || 'Failed to parse file');
        setIsLoading(false);
        return;
      }

      const parsedData = result.data;

      // Generate fields with auto-detected types
      const detectedFields: Field[] = parsedData.columns.map((col) => {
        const typeInfo = detectFieldType(parsedData.data, col);
        // Format field name: capitalize first letter, replace underscores with spaces
        const formattedName = col
          .split('_')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
          .join(' ');

        return {
          fid: col,
          name: formattedName,
          semanticType: typeInfo.semanticType,
          analyticType: typeInfo.analyticType,
        };
      });

      // Update state with new data
      console.log('File parsed successfully:', {
        fileName: parsedData.fileName,
        rowCount: parsedData.data.length,
        columnCount: detectedFields.length,
        columns: detectedFields.map(f => f.name)
      });

      setData(parsedData.data as IRow[]);
      setFields(detectedFields);
      setFileName(parsedData.fileName);
      setIsLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
      setIsLoading(false);
    }
  };

  return (
    <>
      <div className="header">
        <h1>Graphic Walker Data Explorer</h1>
        <div className="info-panel">
          <div className="info-item">
            <span className="info-label">File:</span>
            <span className="info-value">{fileName}</span>
          </div>
          <FileSelector onFileSelected={handleFileSelected} isLoading={isLoading} />
        </div>
      </div>
      {error && (
        <div className="error-banner">
          <strong>Error:</strong> {error}
        </div>
      )}
      <div className="content">
        <div className="graphic-walker-container">
          <GraphicWalker
            key={fileName}
            data={data}
            fields={fields}
            i18nLang="en-US"
          />
        </div>
      </div>
    </>
  );
};

export default GraphicWalkerDemo;
