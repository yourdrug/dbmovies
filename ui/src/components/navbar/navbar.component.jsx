import { Link } from 'react-router-dom';
import './navbar.styles.css'

const Navbar = () => {

    return(
        <div className="navbar">
            <Link className="appName" to='/' style={{ textDecoration: 'none' }}>Название</Link> 
            <input className='search-box' type='searchbox' placeholder='Поиск по всему сайту'></input>
            <a className="logbtn">Войти</a>       
        </div>
        
    )
}

export default Navbar;