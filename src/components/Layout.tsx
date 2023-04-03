import React from "react";
import "./Layout.css";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="Layout">
      <main className="Main">{children}</main>
    </div>
  );
};

export default Layout;
