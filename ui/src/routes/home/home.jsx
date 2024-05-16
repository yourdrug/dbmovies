import { Link } from 'react-router-dom';
import Directory from '../../components/directory/directory';
import './home.css'

const Home = () => {
    const categories = [
        {
          id: 1,
          title: 'Все фильмы',
          imageUrl: 'https://www.megacritic.ru/images/luchshie-filmy-2021.jpg',
          slug: 'movies'
        },
        {
          id: 2,
          title: 'Подборка от админов',
          imageUrl: 'https://www.megacritic.ru/images/luchshie-filmy-2021.jpg',
          slug: 'movies/lists/admins-top'
        }
      ];
    
       

    return(
        <div className='main-wrapper'>
            <Directory categories={categories} />
            <div className='album-choices'>
              <Link style={{textDecoration: "none"}} to={'movies/lists/top-250'}>
                <div className='album-current-choice'>
                  ТОП 250
                </div>
              </Link >
              <Link style={{textDecoration: "none"}} to={'movies/lists/top-500'}>
                <div className='album-current-choice'>
                  ТОП 500
                </div>
              </Link>
            </div>
        </div>
    )
}

export default Home;