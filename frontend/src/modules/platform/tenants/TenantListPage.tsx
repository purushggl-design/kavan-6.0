import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import tenantService, { Tenant, CreateTenantPayload } from '../../../services/tenantService';
import './TenantListPage.css';

type StatusFilter = 'ALL' | 'PENDING' | 'ACTIVE' | 'SUSPENDED' | 'ARCHIVED';

const STATUS_LABELS: Record<string, { label: string; className: string }> = {
  PENDING:   { label: 'Pending',   className: 'badge--pending' },
  APPROVED:  { label: 'Approved',  className: 'badge--approved' },
  ACTIVE:    { label: 'Active',    className: 'badge--active' },
  WARNING:   { label: 'Warning',   className: 'badge--warning' },
  READ_ONLY: { label: 'Read Only', className: 'badge--warning' },
  SUSPENDED: { label: 'Suspended', className: 'badge--suspended' },
  ARCHIVED:  { label: 'Archived',  className: 'badge--archived' },
  DELETED:   { label: 'Deleted',   className: 'badge--archived' },
};

const INITIAL_FORM: CreateTenantPayload = {
  tenant_code: '',
  tenant_name: '',
  company_name: '',
  company_domain: '',
  company_email: '',
  company_phone: '',
  timezone: 'UTC',
  currency: 'USD',
};

export const TenantListPage: React.FC = () => {
  const navigate = useNavigate();
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [filtered, setFiltered] = useState<Tenant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('ALL');
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState<CreateTenantPayload>(INITIAL_FORM);
  const [formError, setFormError] = useState<string | null>(null);
  const [formLoading, setFormLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await tenantService.list();
      setTenants(res.data);
    } catch {
      setError('Failed to load tenants. Check your connection or permissions.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  // Filter + search logic
  useEffect(() => {
    let result = tenants;
    if (statusFilter !== 'ALL') result = result.filter(t => t.tenant_status === statusFilter);
    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(t =>
        t.tenant_name.toLowerCase().includes(q) ||
        t.company_name.toLowerCase().includes(q) ||
        t.tenant_code.toLowerCase().includes(q) ||
        t.company_domain.toLowerCase().includes(q)
      );
    }
    setFiltered(result);
  }, [tenants, statusFilter, search]);

  const handleApprove = async (tenant: Tenant) => {
    if (!window.confirm(`Approve and activate "${tenant.tenant_name}"?`)) return;
    setActionLoading(tenant.id);
    try {
      await tenantService.approve(tenant.id);
      await load();
    } catch {
      alert('Failed to approve tenant.');
    } finally {
      setActionLoading(null);
    }
  };

  const handleSuspend = async (tenant: Tenant) => {
    const reason = window.prompt(`Reason for suspending "${tenant.tenant_name}" (optional):`);
    if (reason === null) return; // cancelled
    setActionLoading(tenant.id);
    try {
      await tenantService.suspend(tenant.id, reason);
      await load();
    } catch {
      alert('Failed to suspend tenant.');
    } finally {
      setActionLoading(null);
    }
  };

  const handleDelete = async (tenant: Tenant) => {
    if (!window.confirm(`DELETE "${tenant.tenant_name}"? This action cannot be undone.`)) return;
    setActionLoading(tenant.id);
    try {
      await tenantService.delete(tenant.id);
      await load();
    } catch {
      alert('Failed to delete tenant.');
    } finally {
      setActionLoading(null);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setFormLoading(true);
    try {
      await tenantService.create(formData);
      setShowModal(false);
      setFormData(INITIAL_FORM);
      await load();
    } catch (err: any) {
      const msg = err?.response?.data?.error || 'Failed to create tenant.';
      setFormError(msg);
    } finally {
      setFormLoading(false);
    }
  };

  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const counts = {
    ALL: tenants.length,
    PENDING: tenants.filter(t => t.tenant_status === 'PENDING').length,
    ACTIVE: tenants.filter(t => t.tenant_status === 'ACTIVE').length,
    SUSPENDED: tenants.filter(t => t.tenant_status === 'SUSPENDED').length,
    ARCHIVED: tenants.filter(t => t.tenant_status === 'ARCHIVED').length,
  };

  return (
    <div className="tenant-list-page">
      {/* Page Header */}
      <div className="page-header">
        <div className="page-header-left">
          <h1 className="page-title">Tenant Management</h1>
          <p className="page-subtitle">Manage all organizations on the KAVAN platform</p>
        </div>
        <button className="btn-primary" onClick={() => setShowModal(true)}>
          <span>+</span> New Tenant
        </button>
      </div>

      {/* Status filter tabs */}
      <div className="filter-tabs">
        {(['ALL', 'PENDING', 'ACTIVE', 'SUSPENDED', 'ARCHIVED'] as StatusFilter[]).map(s => (
          <button
            key={s}
            className={`filter-tab ${statusFilter === s ? 'filter-tab--active' : ''}`}
            onClick={() => setStatusFilter(s)}
          >
            {s === 'ALL' ? 'All Tenants' : s.charAt(0) + s.slice(1).toLowerCase()}
            <span className="filter-tab-count">{counts[s]}</span>
          </button>
        ))}
      </div>

      {/* Search bar */}
      <div className="search-bar">
        <span className="search-icon">🔍</span>
        <input
          type="text"
          placeholder="Search by name, code, domain..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="search-input"
        />
        {search && (
          <button className="search-clear" onClick={() => setSearch('')}>✕</button>
        )}
      </div>

      {/* Error */}
      {error && <div className="error-banner">{error} <button onClick={load}>Retry</button></div>}

      {/* Table */}
      {loading ? (
        <div className="loading-state">
          <div className="spinner" />
          <p>Loading tenants...</p>
        </div>
      ) : filtered.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🏢</div>
          <h3>No tenants found</h3>
          <p>{search || statusFilter !== 'ALL' ? 'Try adjusting your filters.' : 'Create your first tenant to get started.'}</p>
          {!search && statusFilter === 'ALL' && (
            <button className="btn-primary" onClick={() => setShowModal(true)}>Create Tenant</button>
          )}
        </div>
      ) : (
        <div className="tenant-table-wrapper">
          <table className="tenant-table">
            <thead>
              <tr>
                <th>Tenant</th>
                <th>Code</th>
                <th>Domain</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(tenant => {
                const badge = STATUS_LABELS[tenant.tenant_status] ?? { label: tenant.tenant_status, className: 'badge--archived' };
                const isActing = actionLoading === tenant.id;
                return (
                  <tr key={tenant.id} className="tenant-row">
                    <td>
                      <div className="tenant-cell">
                        <div className="tenant-avatar">{tenant.tenant_name.charAt(0).toUpperCase()}</div>
                        <div>
                          <div className="tenant-name">{tenant.tenant_name}</div>
                          <div className="tenant-company">{tenant.company_name}</div>
                        </div>
                      </div>
                    </td>
                    <td><code className="tenant-code">{tenant.tenant_code}</code></td>
                    <td className="tenant-domain">{tenant.company_domain}</td>
                    <td>
                      <span className={`status-badge ${badge.className}`}>{badge.label}</span>
                    </td>
                    <td className="tenant-date">
                      {new Date(tenant.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}
                    </td>
                    <td>
                      <div className="action-group">
                        <button
                          className="action-btn action-btn--view"
                          onClick={() => navigate(`/platform/tenants/${tenant.id}`)}
                          title="View details"
                        >
                          View
                        </button>
                        {tenant.tenant_status === 'PENDING' && (
                          <button
                            className="action-btn action-btn--approve"
                            onClick={() => handleApprove(tenant)}
                            disabled={isActing}
                            title="Approve tenant"
                          >
                            {isActing ? '...' : 'Approve'}
                          </button>
                        )}
                        {tenant.tenant_status === 'ACTIVE' && (
                          <button
                            className="action-btn action-btn--suspend"
                            onClick={() => handleSuspend(tenant)}
                            disabled={isActing}
                            title="Suspend tenant"
                          >
                            {isActing ? '...' : 'Suspend'}
                          </button>
                        )}
                        <button
                          className="action-btn action-btn--delete"
                          onClick={() => handleDelete(tenant)}
                          disabled={isActing}
                          title="Delete tenant"
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Create Tenant Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Create New Tenant</h2>
              <button className="modal-close" onClick={() => setShowModal(false)}>✕</button>
            </div>
            <form className="modal-form" onSubmit={handleCreate}>
              {formError && <div className="form-error">{formError}</div>}
              <div className="form-row">
                <div className="form-group">
                  <label>Tenant Name *</label>
                  <input name="tenant_name" value={formData.tenant_name} onChange={handleFormChange} required placeholder="Acme Corporation" />
                </div>
                <div className="form-group">
                  <label>Tenant Code *</label>
                  <input name="tenant_code" value={formData.tenant_code} onChange={handleFormChange} required placeholder="acme-corp" pattern="[a-z0-9\-]+" title="Lowercase letters, numbers, hyphens only" />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Company Name *</label>
                  <input name="company_name" value={formData.company_name} onChange={handleFormChange} required placeholder="Acme Corp Ltd." />
                </div>
                <div className="form-group">
                  <label>Domain *</label>
                  <input name="company_domain" value={formData.company_domain} onChange={handleFormChange} required placeholder="acme.com" />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Company Email</label>
                  <input name="company_email" type="email" value={formData.company_email} onChange={handleFormChange} placeholder="admin@acme.com" />
                </div>
                <div className="form-group">
                  <label>Phone</label>
                  <input name="company_phone" value={formData.company_phone} onChange={handleFormChange} placeholder="+1-555-000-0000" />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Timezone</label>
                  <select name="timezone" value={formData.timezone} onChange={handleFormChange}>
                    <option value="UTC">UTC</option>
                    <option value="America/New_York">America/New_York</option>
                    <option value="America/Los_Angeles">America/Los_Angeles</option>
                    <option value="Europe/London">Europe/London</option>
                    <option value="Europe/Berlin">Europe/Berlin</option>
                    <option value="Asia/Kolkata">Asia/Kolkata</option>
                    <option value="Asia/Singapore">Asia/Singapore</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Currency</label>
                  <select name="currency" value={formData.currency} onChange={handleFormChange}>
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                    <option value="GBP">GBP</option>
                    <option value="INR">INR</option>
                    <option value="SGD">SGD</option>
                  </select>
                </div>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn-primary" disabled={formLoading}>
                  {formLoading ? 'Creating...' : 'Create Tenant'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
