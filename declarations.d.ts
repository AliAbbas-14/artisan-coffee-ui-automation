// Global TypeScript Declarations for Next.js and React

declare namespace React {
  export type ReactNode =
    | string
    | number
    | boolean
    | null
    | undefined
    | ReactElement<any, any>
    | Iterable<ReactNode>;
  export type ReactElement<P = any, T extends string | JSXElementConstructor<any> = string | JSXElementConstructor<any>> = {
    type: T;
    props: P;
    key: any;
  };
  export type JSXElementConstructor<P> = ((props: P) => ReactElement<any, any> | null) | (new (props: P) => any);
  export type FC<P = {}> = (props: P) => ReactElement<any, any> | null;
  export type CSSProperties = Record<string, any>;
  export type RefObject<T> = { readonly current: T | null };
  export type Dispatch<A> = (value: A) => void;
  export type SetStateAction<S> = S | ((prevState: S) => S);
  export type ChangeEvent<T = Element> = { target: T & { value: string } };
  export type FormEvent<T = Element> = { preventDefault: () => void };
  export type MouseEvent<T = Element> = { preventDefault: () => void; stopPropagation: () => void };
  export function createContext<T>(defaultValue: T): {
    Provider: FC<{ value: T; children?: ReactNode }>;
    Consumer: FC<{ children: (value: T) => ReactNode }>;
  };
  export function useContext<T>(context: { Provider: FC<{ value: T; children?: ReactNode }> }): T;
  export function useState<T>(initialState: T | (() => T)): [T, Dispatch<SetStateAction<T>>];
  export function useEffect(effect: () => void | (() => void), deps?: readonly any[]): void;
  export function useCallback<T extends (...args: any[]) => any>(callback: T, deps: readonly any[]): T;
  export function useMemo<T>(factory: () => T, deps: readonly any[] | undefined): T;
  export function useRef<T>(initialValue: T): { current: T };
  export function useRef<T = unknown>(): { current: T | undefined };
}

declare namespace JSX {
  export interface Element extends React.ReactElement<any, any> {}
  export interface IntrinsicElements {
    [elemName: string]: any;
  }
}

declare module 'react' {
  export = React;
  export as namespace React;
}

declare module 'react-dom' {
  export const render: any;
  export const createPortal: any;
}

declare module 'react/jsx-runtime' {
  export const jsx: any;
  export const jsxs: any;
  export const Fragment: any;
}

declare module 'next' {
  export type Metadata = {
    title?: string;
    description?: string;
    [key: string]: any;
  };
}

declare module 'next/link' {
  import { FC, ReactNode } from 'react';
  const Link: FC<{
    href: string;
    className?: string;
    children?: ReactNode;
    [key: string]: any;
  }>;
  export default Link;
}

declare module 'next/font/google' {
  export function Inter(options?: any): { variable: string; className: string };
  export function Playfair_Display(options?: any): { variable: string; className: string };
}

declare module 'next/server' {
  export class NextResponse {
    static next(init?: any): any;
    static redirect(url: string | URL, status?: number): any;
    static json(body: any, init?: any): any;
  }
  export type NextRequest = any;
}

declare module 'next-auth' {
  export type NextAuthOptions = any;
  export type Session = {
    user: {
      name?: string | null;
      email?: string | null;
      image?: string | null;
      id?: string;
      role?: string;
    };
  };
  export function getServerSession(...args: any[]): Promise<Session | null>;
}

declare module 'next-auth/react' {
  export function useSession(): { data: any; status: 'authenticated' | 'loading' | 'unauthenticated' };
  export function signOut(options?: { callbackUrl?: string }): Promise<void>;
  export function signIn(provider?: string, options?: any): Promise<any>;
  export const SessionProvider: React.FC<{ children?: React.ReactNode; session?: any }>;
}

declare module 'next-auth/middleware' {
  export function withAuth(...args: any[]): any;
}

declare module 'next-auth/providers/credentials' {
  export default function CredentialsProvider(options: any): any;
}

declare module 'framer-motion' {
  export const motion: Record<string, any>;
  export const AnimatePresence: React.FC<{ children?: React.ReactNode; [key: string]: any }>;
  export function useScroll(options?: any): any;
  export function useTransform(...args: any[]): any;
  export function useSpring(...args: any[]): any;
  export function useVelocity(...args: any[]): any;
}

declare module 'bcryptjs' {
  export function hash(s: string, salt: number | string): Promise<string>;
  export function compare(s: string, hash: string): Promise<boolean>;
}

declare module '@prisma/client' {
  export class PrismaClient {
    [key: string]: any;
  }
}

declare module 'tailwindcss' {
  export type Config = Record<string, any>;
}
