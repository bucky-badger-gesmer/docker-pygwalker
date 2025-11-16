import React, { useRef } from 'react';
import './FileSelector.css';

interface FileSelectorProps {
  onFileSelected: (file: File) => void;
  isLoading: boolean;
}

const FileSelector: React.FC<FileSelectorProps> = ({ onFileSelected, isLoading }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileSelected(file);
      // Reset input so the same file can be selected again
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="file-selector">
      <input
        ref={fileInputRef}
        type="file"
        accept=".csv,.json,.xlsx,.xls"
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
      <button
        className="file-select-button"
        onClick={handleButtonClick}
        disabled={isLoading}
      >
        {isLoading ? 'Loading...' : 'Upload File'}
      </button>
      <span className="file-selector-hint">
        Supported formats: CSV, JSON, Excel (.xlsx, .xls)
      </span>
    </div>
  );
};

export default FileSelector;
