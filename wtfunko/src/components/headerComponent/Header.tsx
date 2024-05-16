import { Link } from "react-router-dom"; // Assumendo che tu utilizzi React Router
import { FaSearch, FaShoppingCart, FaUser } from "react-icons/fa";
import "./Header.css";
const Header = () => {
  return (
    <header className="header">
      <div className="header-container">
        <h1 className="logo">WTFunko</h1>
        <nav className="nav">
          <Link to="/store" className="nav-link">
            Store
          </Link>
          <div className="search-box">
            <input type="text" placeholder="Search a product..." />
            <FaSearch className="search-icon" />
          </div>
        </nav>
        <div className="user-actions">
          <Link to="/cart" className="cart-icon">
            <FaShoppingCart />
          </Link>
          <Link to="/profile" className="user-icon">
            <FaUser />
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Header;
