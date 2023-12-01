import { Link } from 'react-router-dom';
import Modal from '../modal/modal.component';
import LoginForm from '../login-form/login-form.component';
import SignUpForm from '../signup-form/signup-form.component';
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
            { !currentUser ? 
            (<div className='auth-module'>
                <a className="logbtn" onClick={() => setActive(true)}>Войти</a> 
                <Modal active={active} setActive={setActive}>
                    <SignUpForm/>
                </Modal>
            </div> 
            ) : (
            <div className='auth-module'>
                <div className='user-avatar'>
                    <img src={currentUser ? currentUser.image : ''} alt='NICHEGO NET'></img>
                </div>
                <Link className="navbar-username" to='/profile' style={{ textDecoration: 'none' }}>{currentUser.username}</Link>
            </div>) }    
        </div>
        
    )
}

export default Navbar;