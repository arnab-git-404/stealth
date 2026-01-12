import { Mail, Globe } from "lucide-react";
import { Link } from "react-router-dom";

export function Footer() {
  const productLinks = [
    { name: "Features", href: "#features" },
    { name: "Pricing", href: "#pricing" },
    { name: "Security", href: "#security" },
    { name: "Integrations", href: "#integrations" },
  ];

  const companyLinks = [
    { name: "About", href: "/about" },
    { name: "Blog", href: "/blog" },
    { name: "Careers", href: "/careers" },
    { name: "Contact", href: "/contact" },
  ];

  const legalLinks = [
    { name: "Privacy Policy", href: "/privacy" },
    { name: "Terms of Service", href: "/terms" },
    { name: "BAA Agreement", href: "/baa" },
  ];

  return (
    <footer className="dark:bg-background-dark border-t border-gray-200 dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-6 lg:px-12 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 lg:gap-12">
          {/* Brand Section */}
          <div className="lg:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="size-8 bg-primary rounded-lg flex items-center justify-center text-white">
                <span className="material-symbols-outlined text-lg">D</span>
              </div>
              <h3 className="text-lg font-bold text-text-main dark:text-white">
                DocuFlow AI
              </h3>
            </div>
            <p className="text-text-sub dark:text-gray-400 text-sm leading-relaxed mb-6 max-w-xs">
              Empowering clinicians with intelligent automation. Secure,
              accurate, and built for modern healthcare.
            </p>
            <div className="flex gap-3">
              <a
                href="mailto:contact@docuflow.ai"
                className="w-10 h-10 rounded-lg bg-gray-100 dark:bg-surface-dark hover:bg-gray-200 dark:hover:bg-gray-700 flex items-center justify-center text-text-sub dark:text-gray-400 hover:text-primary transition-colors"
                aria-label="Email"
              >
                <Mail className="w-5 h-5" />
              </a>
              <a
                href="https://docuflow.ai"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 rounded-lg bg-gray-100 dark:bg-surface-dark hover:bg-gray-200 dark:hover:bg-gray-700 flex items-center justify-center text-text-sub dark:text-gray-400 hover:text-primary transition-colors"
                aria-label="Website"
              >
                <Globe className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Product Links */}
          <div>
            <h4 className="text-sm font-semibold text-text-main dark:text-white uppercase tracking-wider mb-4">
              Product
            </h4>
            <ul className="space-y-3">
              {productLinks.map((link) => (
                <li key={link.name}>
                  <a
                    href={link.href}
                    className="text-text-sub dark:text-gray-400 hover:text-primary dark:hover:text-primary text-sm transition-colors"
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h4 className="text-sm font-semibold text-text-main dark:text-white uppercase tracking-wider mb-4">
              Company
            </h4>
            <ul className="space-y-3">
              {companyLinks.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.href}
                    className="text-text-sub dark:text-gray-400 hover:text-primary dark:hover:text-primary text-sm transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal Links */}
          <div>
            <h4 className="text-sm font-semibold text-text-main dark:text-white uppercase tracking-wider mb-4">
              Legal
            </h4>
            <ul className="space-y-3">
              {legalLinks.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.href}
                    className="text-text-sub dark:text-gray-400 hover:text-primary dark:hover:text-primary text-sm transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-gray-200 dark:border-gray-800 flex justify-center items-center gap-4">
          <p className="text-text-sub dark:text-gray-400 text-sm">
            © {new Date().getFullYear()} DocuFlow AI Inc. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
