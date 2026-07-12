import { apiClient as api } from '@/api/apiClient';

export interface Product {
  id: string;
  code: string;
  name: string;
  slug: string;
  short_description: string;
  description: string;
  category: string | null;
  vendor: string;
  status: 'DRAFT' | 'PUBLISHED' | 'ARCHIVED';
  visibility: 'PUBLIC' | 'PRIVATE' | 'TENANT_SPECIFIC';
  logo: string;
  banner: string;
  icon: string;
  website: string;
  documentation_url: string;
  license_type: string;
  pricing_model: string;
  created_at: string;
  updated_at: string;
  listing?: {
    is_featured: boolean;
    is_trending: boolean;
    downloads: number;
    rating: string;
    reviews_count: number;
  };
}

export interface ProductCategory {
  id: string;
  name: string;
  slug: string;
  description: string;
}

const marketplaceService = {
  /** List all published products (public marketplace browse) */
  listProducts: async (params?: { search?: string; category?: string }): Promise<Product[]> => {
    const res = await api.get('/marketplace/', { params });
    // DRF ViewSet returns results array
    return res.data.results ?? res.data.data ?? res.data;
  },

  /** Get a single product detail */
  getProduct: async (id: string): Promise<Product> => {
    const res = await api.get(`/marketplace/${id}/`);
    return res.data.data ?? res.data;
  },

  /** Search products by query */
  search: async (q: string): Promise<Product[]> => {
    const res = await api.get('/marketplace/search/', { params: { q } });
    return res.data.results ?? res.data.data ?? res.data;
  },

  /** Get featured products */
  getFeatured: async (): Promise<Product[]> => {
    const res = await api.get('/marketplace/featured/');
    return res.data.results ?? res.data.data ?? res.data;
  },

  /** Get latest products */
  getLatest: async (): Promise<Product[]> => {
    const res = await api.get('/marketplace/latest/');
    return res.data.results ?? res.data.data ?? res.data;
  },

  /** Subscribe to a product */
  subscribe: async (productId: string): Promise<{ message: string }> => {
    const res = await api.post(`/marketplace/${productId}/subscribe/`);
    return res.data;
  },

  /** Get my subscriptions */
  getSubscriptions: async (): Promise<Product[]> => {
    const res = await api.get('/marketplace/subscriptions/');
    return res.data.results ?? res.data.data ?? res.data;
  },

  // ---- Platform Admin: manage all products ----

  /** List all products (platform admin, includes DRAFT + ARCHIVED) */
  listAllProducts: async (): Promise<Product[]> => {
    const res = await api.get('/platform/products/');
    return res.data.results ?? res.data.data ?? res.data;
  },

  /** Publish a product */
  publish: async (productId: string): Promise<void> => {
    await api.post(`/platform/products/${productId}/publish/`);
  },

  /** Archive a product */
  archive: async (productId: string): Promise<void> => {
    await api.post(`/platform/products/${productId}/archive/`);
  },
};

export default marketplaceService;
