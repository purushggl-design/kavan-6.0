import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';

export function Breadcrumbs() {
  const location = useLocation();
  const paths = location.pathname.split('/').filter(Boolean);

  if (paths.length === 0) return null;

  return (
    <div className="flex items-center text-sm text-muted-foreground">
      <Link to="/" className="hover:text-foreground transition-colors flex items-center">
        <Home className="w-4 h-4" />
      </Link>
      
      {paths.map((path, index) => {
        const isLast = index === paths.length - 1;
        const href = `/${paths.slice(0, index + 1).join('/')}`;
        const title = path.charAt(0).toUpperCase() + path.slice(1).replace(/-/g, ' ');

        return (
          <React.Fragment key={path}>
            <ChevronRight className="w-4 h-4 mx-1" />
            {isLast ? (
              <span className="font-medium text-foreground">{title}</span>
            ) : (
              <Link to={href} className="hover:text-foreground transition-colors">
                {title}
              </Link>
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
}
