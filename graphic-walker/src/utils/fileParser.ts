import Papa from 'papaparse';
import * as XLSX from 'xlsx';

export interface ParsedData {
  data: Record<string, any>[];
  fileName: string;
  rowCount: number;
  columnCount: number;
  columns: string[];
}

export interface FileParseResult {
  success: boolean;
  data?: ParsedData;
  error?: string;
}

/**
 * Parse CSV file using PapaParse
 */
const parseCSV = (file: File): Promise<Record<string, any>[]> => {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: (results) => {
        if (results.errors.length > 0) {
          reject(new Error(`CSV parsing errors: ${results.errors.map(e => e.message).join(', ')}`));
        } else {
          resolve(results.data as Record<string, any>[]);
        }
      },
      error: (error) => {
        reject(error);
      },
    });
  });
};

/**
 * Parse Excel file using SheetJS
 */
const parseExcel = async (file: File): Promise<Record<string, any>[]> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const data = e.target?.result;
        const workbook = XLSX.read(data, { type: 'binary' });

        // Get the first sheet
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];

        // Convert to JSON
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { defval: null });
        resolve(jsonData as Record<string, any>[]);
      } catch (error) {
        reject(new Error(`Excel parsing error: ${error}`));
      }
    };

    reader.onerror = () => {
      reject(new Error('Failed to read Excel file'));
    };

    reader.readAsBinaryString(file);
  });
};

/**
 * Parse JSON file
 */
const parseJSON = (file: File): Promise<Record<string, any>[]> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const text = e.target?.result as string;
        const jsonData = JSON.parse(text);

        // Ensure it's an array
        if (Array.isArray(jsonData)) {
          resolve(jsonData);
        } else {
          reject(new Error('JSON file must contain an array of objects'));
        }
      } catch (error) {
        reject(new Error(`JSON parsing error: ${error}`));
      }
    };

    reader.onerror = () => {
      reject(new Error('Failed to read JSON file'));
    };

    reader.readAsText(file);
  });
};

/**
 * Main file parser that handles multiple formats
 */
export const parseDataFile = async (file: File): Promise<FileParseResult> => {
  try {
    const fileExtension = file.name.split('.').pop()?.toLowerCase();
    let data: Record<string, any>[];

    switch (fileExtension) {
      case 'csv':
        data = await parseCSV(file);
        break;

      case 'xlsx':
      case 'xls':
        data = await parseExcel(file);
        break;

      case 'json':
        data = await parseJSON(file);
        break;

      default:
        return {
          success: false,
          error: `Unsupported file format: .${fileExtension}. Supported formats: CSV, XLSX, XLS, JSON`,
        };
    }

    // Validate data
    if (!data || data.length === 0) {
      return {
        success: false,
        error: 'File is empty or contains no valid data',
      };
    }

    // Extract column names from first row
    const columns = Object.keys(data[0]);

    return {
      success: true,
      data: {
        data,
        fileName: file.name,
        rowCount: data.length,
        columnCount: columns.length,
        columns,
      },
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error occurred',
    };
  }
};

/**
 * Detect field types for GraphicWalker
 */
export const detectFieldType = (
  data: Record<string, any>[],
  fieldName: string
): { semanticType: 'nominal' | 'ordinal' | 'quantitative' | 'temporal'; analyticType: 'dimension' | 'measure' } => {
  // Sample first few non-null values
  const sampleSize = Math.min(10, data.length);
  const samples = data
    .slice(0, sampleSize)
    .map(row => row[fieldName])
    .filter(val => val != null && val !== '');

  if (samples.length === 0) {
    return { semanticType: 'nominal', analyticType: 'dimension' };
  }

  // Check if all samples are numbers
  const allNumbers = samples.every(val => typeof val === 'number' || !isNaN(Number(val)));
  if (allNumbers) {
    return { semanticType: 'quantitative', analyticType: 'measure' };
  }

  // Check if it looks like a date
  const datePatterns = [
    /^\d{4}-\d{2}-\d{2}/, // ISO date
    /^\d{1,2}\/\d{1,2}\/\d{4}/, // US date
    /^\d{4}\/\d{2}\/\d{2}/, // Alternative date format
  ];

  const looksLikeDate = samples.some(val => {
    const str = String(val);
    return datePatterns.some(pattern => pattern.test(str)) || !isNaN(Date.parse(str));
  });

  if (looksLikeDate) {
    return { semanticType: 'temporal', analyticType: 'dimension' };
  }

  // Default to nominal dimension
  return { semanticType: 'nominal', analyticType: 'dimension' };
};
