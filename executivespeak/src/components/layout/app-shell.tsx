"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Mic,
  MessageSquare,
  Crown,
  Code2,
  Presentation,
  Briefcase,
  Users,
  Zap,
  Mail,
  ClipboardCheck,
  BookHeart,
  BookOpen,
  AudioLines,
  TrendingUp,
  AlertCircle,
  Library,
  Settings,
} from "lucide-react";

const NAV = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/practice", label: "Practice", icon: Mic },
  { href: "/conversation", label: "Conversation", icon: MessageSquare },
  { href: "/meeting", label: "Meeting", icon: Users },
  { href: "/impromptu", label: "Impromptu", icon: Zap },
  { href: "/writing", label: "Email & Chat", icon: Mail },
  { href: "/leadership", label: "Leadership", icon: Crown },
  { href: "/technical", label: "Technical English", icon: Code2 },
  { href: "/presentation", label: "Presentation", icon: Presentation },
  { href: "/storytelling", label: "Storytelling", icon: BookHeart },
  { href: "/interview", label: "Interview", icon: Briefcase },
  { href: "/vocabulary", label: "Vocabulary", icon: BookOpen },
  { href: "/pronunciation", label: "Pronunciation", icon: AudioLines },
  { href: "/progress", label: "Progress", icon: TrendingUp },
  { href: "/assessment", label: "Weekly assessment", icon: ClipboardCheck },
  { href: "/mistakes", label: "Mistakes", icon: AlertCircle },
  { href: "/phrasebook", label: "Phrasebook", icon: Library },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="flex min-h-screen">
        <aside className="hidden w-64 shrink-0 border-r border-border/60 bg-card/30 p-4 lg:block">
          <Link href="/dashboard" className="mb-8 block px-2">
            <span className="text-lg font-semibold tracking-tight">ExecutiveSpeak</span>
            <span className="mt-1 block text-xs text-muted-foreground">AI Communication Coach</span>
          </Link>
          <nav className="space-y-1">
            {NAV.map(({ href, label, icon: Icon }) => (
              <Link
                key={href}
                href={href}
                className={cn(
                  "flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors",
                  pathname === href || pathname.startsWith(href + "/")
                    ? "bg-primary/10 text-primary font-medium"
                    : "text-muted-foreground hover:bg-accent hover:text-foreground",
                )}
              >
                <Icon className="h-4 w-4" />
                {label}
              </Link>
            ))}
          </nav>
        </aside>
        <main className="flex-1 overflow-auto">{children}</main>
      </div>
    </div>
  );
}
