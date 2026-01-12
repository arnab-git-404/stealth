import AppRoutes from "./AppRoutes";
import { Footer } from "./components/Footer";
import { Navbar } from "./components/Navbar";
import { ThemeProvider } from "./components/theme-provider";
import { ReactLenis } from 'lenis/react'


export default function App() {
  return (
    <>
      <ThemeProvider defaultTheme="system" storageKey="docuflow-theme">
        <ReactLenis root />
        <Navbar />
        <AppRoutes />
        <Footer />
      </ThemeProvider>
    </>
  );
}
