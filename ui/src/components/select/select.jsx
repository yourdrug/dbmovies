import Select from 'react-select';
import './select.css'

function FilterSelect({ options, defaultValue, onChange }) {
  return (
    <Select
      className="react-select-container"
      classNamePrefix="react-select"
      options={options}
      defaultValue={defaultValue}
      onChange={onChange}
    />
  );
}

export default FilterSelect;