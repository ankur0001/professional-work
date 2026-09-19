import "next-auth";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      email?: string | null;
      name?: string | null;
      demo?: boolean;
    };
  }

  interface User {
    demo?: boolean;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    id?: string;
    demo?: boolean;
  }
}
