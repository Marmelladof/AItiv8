import Navbar from "../navbar/Navbar";
import Form from "../form/Form";
import styles from "./Home.module.css";
import ViewCard from "../viewCard/ViewCard";

function Home() {
  return (
    <div className={styles.mainContainer}>
      <div className={styles.workContainer}>
        <ViewCard route="Form" titulo="Ola"></ViewCard>
        <ViewCard titulo="Ola"></ViewCard>
      </div>
    </div>
  );
}

export default Home;
