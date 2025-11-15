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

  return (
    <div className="graphic-walker-container">
      <GraphicWalker
        data={data}
        fields={fields}
        i18nLang="en-US"
      />
    </div>
  );
};

export default GraphicWalkerDemo;
