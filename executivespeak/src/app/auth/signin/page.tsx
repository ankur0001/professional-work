import { Suspense } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { DEMO_CREDENTIALS } from "@/lib/demo/demo-store";
import { SignInForm } from "./sign-in-form";

export default function SignInPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Welcome back</CardTitle>
          <CardDescription>
            Demo: <code className="text-xs">{DEMO_CREDENTIALS.email}</code> /{" "}
            <code className="text-xs">{DEMO_CREDENTIALS.password}</code>
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Suspense fallback={<p className="text-sm text-muted-foreground">Loading…</p>}>
            <SignInForm />
          </Suspense>
        </CardContent>
      </Card>
    </div>
  );
}
