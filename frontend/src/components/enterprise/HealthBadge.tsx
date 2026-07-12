import React from "react"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

export type HealthStatus = "healthy" | "degraded" | "critical" | "unknown"

export interface HealthBadgeProps {
  status: HealthStatus
  label?: string
  className?: string
}

export function HealthBadge({ status, label, className }: HealthBadgeProps) {
  const statusConfig = {
    healthy: {
      color: "bg-success/15 text-success hover:bg-success/25 border-success/30",
      defaultLabel: "Healthy",
    },
    degraded: {
      color: "bg-warning/15 text-warning-foreground hover:bg-warning/25 border-warning/30",
      defaultLabel: "Degraded",
    },
    critical: {
      color: "bg-destructive/15 text-destructive hover:bg-destructive/25 border-destructive/30",
      defaultLabel: "Critical",
    },
    unknown: {
      color: "bg-muted text-muted-foreground border-muted-foreground/30",
      defaultLabel: "Unknown",
    },
  }

  const config = statusConfig[status] || statusConfig.unknown

  return (
    <Badge
      variant="outline"
      className={cn("font-medium transition-colors border", config.color, className)}
    >
      <span
        className={cn(
          "mr-1.5 h-2 w-2 rounded-full",
          status === "healthy" && "bg-success",
          status === "degraded" && "bg-warning",
          status === "critical" && "bg-destructive",
          status === "unknown" && "bg-muted-foreground"
        )}
        aria-hidden="true"
      />
      {label || config.defaultLabel}
    </Badge>
  )
}
