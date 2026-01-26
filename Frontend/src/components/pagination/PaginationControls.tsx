import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import '../../styles/components/Pagination.css';

interface PaginationControlsProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export const PaginationControls: React.FC<PaginationControlsProps> = ({
  currentPage,
  totalPages,
  onPageChange
}) => {
  if (totalPages <= 1) return null;

  const renderPageButton = (page: number) => (
    <button
      key={page}
      onClick={() => onPageChange(page)}
      className={`pagination-page ${page === currentPage ? 'active' : ''}`}
      aria-label={`Go to page ${page}`}
      aria-current={page === currentPage ? 'page' : undefined}
    >
      {page}
    </button>
  );

  const renderPageNumbers = () => {
    const pages = [];

    for (let page = 1; page <= totalPages; page++) {
      if (
        page === 1 ||
        page === totalPages ||
        (page >= currentPage - 1 && page <= currentPage + 1)
      ) {
        pages.push(renderPageButton(page));
      } else if (page === currentPage - 2 || page === currentPage + 2) {
        pages.push(<span key={`ellipsis-${page}`} className="pagination-ellipsis">...</span>);
      }
    }

    return pages;
  };

  return (
    <div className="pagination-controls">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="pagination-btn"
        aria-label="Previous page"
      >
        <ChevronLeft className="pagination-icon" />
        Previous
      </button>

      <div className="pagination-pages">
        {renderPageNumbers()}
      </div>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="pagination-btn"
        aria-label="Next page"
      >
        Next
        <ChevronRight className="pagination-icon" />
      </button>
    </div>
  );
};
