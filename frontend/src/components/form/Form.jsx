import { useForm } from "react-hook-form";
import { useState } from "react";
import { postCrop } from "../../api/apiList";
const dados = [
  { label: "Area", type: "number" },
  {
    label: "N",
    type: "number",
  },
  {
    label: "P",
    type: "number",
  },
  {
    label: "Temperature",
    type: "number",
  },
  {
    label: "Humidity",
    type: "number",
  },
  {
    label: "PH",
    type: "number",
  },
  {
    label: "Rainfall",
    type: "number",
  },
];
function Form(props) {
  const { register, handleSubmit } = useForm();

  return (
    <div>
      <section class="max-w-4xl p-6 mx-auto bg-indigo-600 rounded-md shadow-md dark:bg-gray-800 mt-20">
        <h1 class="text-xl font-bold text-white capitalize dark:text-white">
          Campo {props.formId}
        </h1>
        <form onChange={handleSubmit((data) => formSaveHandler(data))}>
          <div class="grid grid-cols-1 gap-5 mt-4 sm:grid-cols-3">
            {dados.map((dado, i) => (
              <div>
                <label class="text-white dark:text-gray-200" for={dado.label}>
                  {dado.label}
                </label>
                <input
                  {...register(dado.label, { required: true })}
                  id={dado.label}
                  type={dado.type}
                  class="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring"
                />
              </div>
            ))}
          </div>
          <div class="flex justify-end mt-6" />
        </form>
      </section>
    </div>
  );

  function formSaveHandler(Parameters) {
    let Space = props.formId;
    let Field = { Space, Parameters };
    props.onFormChange(Field, props.formId);
  }
}

export default Form;
