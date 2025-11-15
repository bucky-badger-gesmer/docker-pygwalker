// Type declarations for @kanaries/graphic-walker
// This helps with TypeScript autocomplete and type safety

declare module '@kanaries/graphic-walker' {
  import { FC } from 'react';

  export interface IRow {
    [key: string]: any;
  }

  export interface IField {
    fid: string;
    name: string;
    semanticType: 'temporal' | 'nominal' | 'ordinal' | 'quantitative';
    analyticType: 'dimension' | 'measure';
  }

  export interface GraphicWalkerProps {
    data: IRow[];
    fields: IField[];
    chart?: any[];
    i18nLang?: string;
    dark?: 'light' | 'dark';
    themeKey?: string;
    appearance?: 'light' | 'dark';
  }

  export const GraphicWalker: FC<GraphicWalkerProps>;
}

declare module '@kanaries/graphic-walker/interfaces' {
  export interface IRow {
    [key: string]: any;
  }
}
