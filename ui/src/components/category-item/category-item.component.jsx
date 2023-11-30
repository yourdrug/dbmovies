import { Link } from 'react-router-dom';
import './category-item.styles.scss';

const CategoryItem = ({ category }) => {
  const { imageUrl, title, slug } = category;
  return (
    <div className='category-container'>
      <div
        className='background-image'
        style={{
          backgroundColor: '#3D3C3A',
        }}
      />
      <div className='category-body-container'>
        <Link to={slug} style={{ textDecoration: 'none' }}><h2>{title}</h2></Link>
      </div>
    </div>
  );
};

export default CategoryItem;