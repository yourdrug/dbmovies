import { Link } from 'react-router-dom';
import Modal from '../modal/modal.component';
import LoginForm from '../login-form/login-form.component';
import './navbar.styles.css';
import { useState, useContext } from 'react';

import { UserContext } from '../../context/user.context';

const Navbar = () => {
    const [active, setActive] = useState(false);
    
    const { currentUser } = useContext(UserContext);
    console.log(currentUser);
    

    return(
        <div className="navbar">
            <Link className="appName" to='/' style={{ textDecoration: 'none' }}>Название</Link> 
            <input className='search-box' type='searchbox' placeholder='Поиск по всему сайту'></input>
            <a className="logbtn" onClick={() => setActive(true)}>Войти</a> 
            <Modal active={active} setActive={setActive}>
                <LoginForm/>
            </Modal>      
        </div>
        
    )
}

export default Navbar;