import { Link } from 'react-router-dom';
import './category-item.styles.scss';

const CategoryItem = ({ category }) => {
  const { imageUrl, title, slug } = category;
  return (
    <div className='category-container'>
      <Link to={slug} style={{ textDecoration: 'none', backgroundColor: '#3D3C3A'}}
        className='background-image'/>
      <div className='category-body-container'>
        <h2>{title}</h2>
      </div>
    </div>
  );
};

export default CategoryItem;