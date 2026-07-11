import React, { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import marketplaceService, { Product } from '../../../services/marketplaceService';
import './MarketplacePage.css';

const STATUS_ICON: Record<string, string> = {
  PUBLISHED: '🟢',
  DRAFT: '🟡',
  ARCHIVED: '⚫',
};

const PRICING_LABEL: Record<string, string> = {
  SUBSCRIPTION: 'Subscription',
  ONE_TIME: 'One-time',
  FREE: 'Free',
  USAGE_BASED: 'Usage-based',
};

const LICENSE_COLOR: Record<string, string> = {
  ENTERPRISE: '#7c3aed',
  PROFESSIONAL: '#06b6d4',
  COMMUNITY: '#22c55e',
};

export const MarketplacePage: React.FC = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<'ALL' | 'PUBLISHED' | 'DRAFT' | 'ARCHIVED'>('PUBLISHED');

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        setError(null);
        // Platform admin can see all products
        const data = await marketplaceService.listAllProducts();
        setProducts(data);
      } catch {
        // Fallback: try public marketplace endpoint
        try {
          const data = await marketplaceService.listProducts();
          setProducts(data);
        } catch {
          setError('Failed to load marketplace products.');
        }
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const filtered = useMemo(() => {
    let result = products;
    if (statusFilter !== 'ALL') result = result.filter(p => p.status === statusFilter);
    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(p =>
        p.name.toLowerCase().includes(q) ||
        p.short_description.toLowerCase().includes(q) ||
        p.vendor.toLowerCase().includes(q) ||
        p.code.toLowerCase().includes(q)
      );
    }
    return result;
  }, [products, statusFilter, search]);

  const counts = {
    ALL: products.length,
    PUBLISHED: products.filter(p => p.status === 'PUBLISHED').length,
    DRAFT: products.filter(p => p.status === 'DRAFT').length,
    ARCHIVED: products.filter(p => p.status === 'ARCHIVED').length,
  };

  return (
    <div className="marketplace-page">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">Marketplace</h1>
          <p className="page-subtitle">Browse and manage the KAVAN product catalog</p>
        </div>
      </div>

      {/* Status filter tabs */}
      <div className="filter-tabs">
        {(['ALL', 'PUBLISHED', 'DRAFT', 'ARCHIVED'] as const).map(s => (
          <button
            key={s}
            className={`filter-tab ${statusFilter === s ? 'filter-tab--active' : ''}`}
            onClick={() => setStatusFilter(s)}
          >
            {s === 'ALL' ? 'All Products' : s.charAt(0) + s.slice(1).toLowerCase()}
            <span className="filter-tab-count">{counts[s]}</span>
          </button>
        ))}
      </div>

      {/* Search */}
      <div className="search-bar">
        <span className="search-icon">🔍</span>
        <input
          type="text"
          placeholder="Search products by name, vendor, code..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="search-input"
        />
        {search && <button className="search-clear" onClick={() => setSearch('')}>✕</button>}
      </div>

      {/* Content */}
      {error && <div className="error-banner">{error}</div>}

      {loading ? (
        <div className="loading-state">
          <div className="spinner" />
          <p>Loading products...</p>
        </div>
      ) : filtered.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🛒</div>
          <h3>No products found</h3>
          <p>
            {search || statusFilter !== 'ALL'
              ? 'Try adjusting your search or filters.'
              : 'Run bootstrap_platform to seed demo products.'}
          </p>
          {!search && statusFilter === 'ALL' && (
            <div className="empty-hint">
              <code>python manage.py bootstrap_platform</code>
            </div>
          )}
        </div>
      ) : (
        <>
          <p className="results-count">Showing {filtered.length} product{filtered.length !== 1 ? 's' : ''}</p>
          <div className="product-grid">
            {filtered.map(product => (
              <div
                key={product.id}
                className="product-card"
                onClick={() => navigate(`/platform/marketplace/${product.id}`)}
              >
                {/* Card header */}
                <div className="product-card-header">
                  <div className="product-icon">
                    {product.logo
                      ? <img src={product.logo} alt={product.name} />
                      : <span>{product.name.charAt(0)}</span>}
                  </div>
                  <div className="product-badges">
                    <span className={`product-status product-status--${product.status.toLowerCase()}`}>
                      {STATUS_ICON[product.status]} {product.status}
                    </span>
                    {product.listing?.is_featured && (
                      <span className="product-featured">⭐ Featured</span>
                    )}
                  </div>
                </div>

                {/* Product info */}
                <div className="product-info">
                  <h3 className="product-name">{product.name}</h3>
                  <p className="product-description">
                    {product.short_description || product.description?.slice(0, 100) || 'No description available.'}
                  </p>
                </div>

                {/* Product meta */}
                <div className="product-meta">
                  <div className="product-meta-row">
                    <span className="meta-label">Vendor</span>
                    <span className="meta-value">{product.vendor || 'Unknown'}</span>
                  </div>
                  <div className="product-meta-row">
                    <span className="meta-label">Pricing</span>
                    <span className="meta-value">{PRICING_LABEL[product.pricing_model] || product.pricing_model || '—'}</span>
                  </div>
                  {product.license_type && (
                    <div className="product-meta-row">
                      <span className="meta-label">License</span>
                      <span
                        className="meta-value meta-license"
                        style={{ color: LICENSE_COLOR[product.license_type] || '#94a3b8' }}
                      >
                        {product.license_type}
                      </span>
                    </div>
                  )}
                </div>

                {/* Card footer */}
                <div className="product-card-footer">
                  <button
                    className="card-action-btn card-action-btn--view"
                    onClick={e => { e.stopPropagation(); navigate(`/platform/marketplace/${product.id}`); }}
                  >
                    View Details →
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};
