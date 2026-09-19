import type { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import bcrypt from "bcryptjs";
import { getPrisma } from "@/lib/db";
import { DEMO_CREDENTIALS, isDemoEmail } from "@/lib/demo/demo-store";
import { isDemoMode } from "@/lib/config";

export const authOptions: NextAuthOptions = {
  session: { strategy: "jwt" },
  pages: {
    signIn: "/auth/signin",
  },
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        const email = credentials?.email?.toLowerCase().trim();
        const password = credentials?.password ?? "";
        if (!email || !password) return null;

        if (isDemoMode() && email === DEMO_CREDENTIALS.email && password === DEMO_CREDENTIALS.password) {
          return {
            id: "demo-user",
            email: DEMO_CREDENTIALS.email,
            name: "Demo Engineer",
            demo: true,
          };
        }

        const prisma = await getPrisma();
        if (!prisma) {
          if (isDemoEmail(email) && password === DEMO_CREDENTIALS.password) {
            return { id: "demo-user", email, name: "Demo User", demo: true };
          }
          return null;
        }

        const user = await prisma.user.findUnique({ where: { email } });
        if (!user?.passwordHash) return null;
        const valid = await bcrypt.compare(password, user.passwordHash);
        if (!valid) return null;
        return { id: user.id, email: user.email, name: user.name ?? undefined };
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.demo = (user as { demo?: boolean }).demo ?? false;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        session.user.demo = Boolean(token.demo);
      }
      return session;
    },
  },
};
