import React from "react"
import { SearchX, FileX, ShieldX, Icon } from "lucide-react"
import { cn } from "@/lib/utils"

export type EmptyStateVariant = "search" | "file" | "security" | "default"

export interface EmptyStateProps {
  title: string
  description: string
  variant?: EmptyStateVariant
  icon?: React.ReactNode
  action?: React.ReactNode
  className?: string
}

export function EmptyState({
  title,
  description,
  variant = "default",
  icon,
  action,
  className,
}: EmptyStateProps) {
  
  const getIcon = () => {
    if (icon) return icon
    
    switch (variant) {
      case "search":
        return <SearchX className="h-10 w-10 text-muted-foreground/60" />
      case "file":
        return <FileX className="h-10 w-10 text-muted-foreground/60" />
      case "security":
        return <ShieldX className="h-10 w-10 text-muted-foreground/60" />
      default:
        return <FileX className="h-10 w-10 text-muted-foreground/60" />
    }
  }

  return (
    <div
      className={cn(
        "flex min-h-[300px] flex-col items-center justify-center rounded-md border border-dashed border-border bg-card/30 p-8 text-center animate-in fade-in-50",
        className
      )}
    >
      <div className="flex h-20 w-20 items-center justify-center rounded-full bg-muted/50 mb-4">
        {getIcon()}
      </div>
      <h3 className="text-lg font-semibold text-foreground mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground max-w-md mb-6">
        {description}
      </p>
      {action && <div>{action}</div>}
    </div>
  )
}
