import './modal.css'

const Modal = ({active, setActive, children}) =>{
    return(
        <div className={active? 'modal-for-everything active' : 'modal-for-everything'} onClick={()=> setActive(false)}>
            <div className={active? 'modal-content active' : 'modal-content'} onClick={e => e.stopPropagation()}>
                {children}
            </div>
        </div>
    );
};

export default Modal