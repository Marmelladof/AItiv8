import Form from "../form/Form";
import { useState, useEffect } from "react";
import { postCrop } from "../../api/apiList";
import { saveForm } from "../../redux/FormSlicer";
import { useSelector, useDispatch, state } from "react-redux";

function FormPage() {
  const [formData, setFormData] = useState([]);

  function handleChange(formResult, formId) {
    formData[formId] = formResult;
    setFormData([...formData]);
  }

  return (
    <span>
      {formData.map((item, index) => (
        <div>
          <Form
            formId={index}
            onFormChange={(formResult, formId) =>
              handleChange(formResult, formId)
            }
          />
          <p>{JSON.stringify(item)}</p>
        </div>
      ))}
      <div class="mx-14 grid grid-cols-4 gap-20 relative">
        <button
          class="px-6 py-2 leading-5 text-white transition-colors duration-200 transform bg-pink-500 rounded-md hover:bg-pink-700 focus:outline-none "
          onClick={() => {
            let Space = formData.length;
            formData.push({ Space });
            setFormData([...formData]);
          }}
        >
          Add Form
        </button>
        <button
          class="right-0 absolute px-6 py-2 leading-5 text-white transition-colors duration-200 transform bg-pink-500 rounded-md hover:bg-pink-700  "
          onClick={() => {
            console.log(formData);
            postCrop(formData);
          }}
        >
          Send
        </button>
      </div>
    </span>
  );
}

export default FormPage;
