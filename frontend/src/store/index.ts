import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
  },
  // AuthState is hydrated from localStorage in initialState, and tokens
  // are non-serializable-safe strings, so no special middleware config needed.
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
