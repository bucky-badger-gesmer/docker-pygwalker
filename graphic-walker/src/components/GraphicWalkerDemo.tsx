import { GraphicWalker } from '@kanaries/graphic-walker';
import type { IRow } from '@kanaries/graphic-walker/interfaces';
import { sampleData } from '../data/sampleData';

const GraphicWalkerDemo: React.FC = () => {
  // Convert our sample data to the format GraphicWalker expects
  const data: IRow[] = sampleData.map((record) => ({
    date: record.date,
    product: record.product,
    category: record.category,
    region: record.region,
    sales: record.sales,
    quantity: record.quantity,
    profit: record.profit,
  }));

  // Define fields metadata for GraphicWalker
  // This tells GraphicWalker about the data types and semantic types of each field
  const fields = [
    {
      fid: 'date',
      name: 'Date',
      semanticType: 'temporal' as const,
      analyticType: 'dimension' as const,
    },
    {
      fid: 'product',
      name: 'Product',
      semanticType: 'nominal' as const,
      analyticType: 'dimension' as const,
    },
    {
      fid: 'category',
      name: 'Category',
      semanticType: 'nominal' as const,
      analyticType: 'dimension' as const,
    },
    {
      fid: 'region',
      name: 'Region',
      semanticType: 'nominal' as const,
      analyticType: 'dimension' as const,
    },
    {
      fid: 'sales',
      name: 'Sales',
      semanticType: 'quantitative' as const,
      analyticType: 'measure' as const,
    },
    {
      fid: 'quantity',
      name: 'Quantity',
      semanticType: 'quantitative' as const,
      analyticType: 'measure' as const,
    },
    {
      fid: 'profit',
      name: 'Profit',
      semanticType: 'quantitative' as const,
      analyticType: 'measure' as const,
    },
  ];

  // Calculate data statistics
  const rowCount = sampleData.length;
  const columnCount = fields.length;
  const columnNames = fields.map(f => f.name).join(', ');
  const fileName = 'sample_data.csv';

  return (
    <>
      <div className="header">
        <h1>Graphic Walker Data Explorer</h1>
        <div className="info-panel">
          <div className="info-item">
            <span className="info-label">File:</span>
            <span className="info-value">{fileName}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Rows:</span>
            <span className="info-value">{rowCount.toLocaleString()}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Columns:</span>
            <span className="info-value">{columnCount}</span>
          </div>
          <div className="columns-info">
            <span className="info-label">Fields:</span>
            <span className="columns-list" title={columnNames}>{columnNames}</span>
          </div>
        </div>
      </div>
      <div className="content">
        <div className="graphic-walker-container">
          <GraphicWalker
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
