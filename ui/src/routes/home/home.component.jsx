import Directory from '../../components/directory/directory.component';
import './home.styles.css'

const Home = () => {
    const categories = [
        {
          id: 1,
          title: 'Фильмы',
          imageUrl: 'https://www.megacritic.ru/images/luchshie-filmy-2021.jpg',
          slug: 'movies'
        },
        {
          id: 2,
          title: 'Сериалы',
          imageUrl: 'https://www.megacritic.ru/images/luchshie-filmy-2021.jpg',
          slug: 'series'
        }
      ];
    
       

    return(
        <div className='main-wrapper'>
            <Directory categories={categories} />
        </div>
    )
}

export default Home;