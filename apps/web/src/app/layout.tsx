import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "VERITAS-600 | Autonomous Trade Finance & UCP 600 Adjudication Terminal",
  description: "Lean Autonomous Trade Finance & UCP 600 Adjudication Engine (Track 03: Reasoning Architecture)",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-slate-100 antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
