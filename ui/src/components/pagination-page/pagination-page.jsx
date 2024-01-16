import './pagination-page.css';
import { useState, useEffect } from 'react'


function Pagination ({setPage, page, numberOfPages}) {
    const [neighbours, setNeighbour] = useState([])

    function changeNeighbour(){
        if (page == 1 && numberOfPages == 1){
            setNeighbour([1])
        }
        else if (page == 1 && numberOfPages == 2){
            setNeighbour([1, 2])
        }
        else if (page == 1 && numberOfPages >=3){
            setNeighbour([1, 2, numberOfPages])
        }
        else if(page == 2 && numberOfPages == 2){
            setNeighbour([1, 2])
        }
        else if(page == 2 && numberOfPages == 3){
            setNeighbour([1, 2, 3])
        }
        else if(page == 2 && numberOfPages == 4){
            setNeighbour([1, 2, 3, 4])
        }
        else if(page == 2 && numberOfPages > 4){
            setNeighbour([1, 2, 3, 4, numberOfPages])
        }
        else if(page == numberOfPages){
            setNeighbour([1, numberOfPages - 1, numberOfPages])
        }
        else if(page == numberOfPages - 1){
            setNeighbour([1, numberOfPages - 2, numberOfPages - 1, numberOfPages])
        }
        else{
            setNeighbour([1, page - 1, page, page + 1, numberOfPages])
        }
    }

    function choosePage(wantedPage){
        setPage(wantedPage);
    }

    useEffect(()=>{
        changeNeighbour();
    }, [page, numberOfPages]);

    return(
        <div className='pagination'>
            {neighbours.map((neighbour, index) => {
                return <button className={`pagination-btn ${page == neighbour ? "page-btn-active" : ""}`} 
                key={index} onClick={()=> choosePage(neighbour)}> {neighbour} </button>;
        })}
        </div>
    )   
}

export default Pagination;