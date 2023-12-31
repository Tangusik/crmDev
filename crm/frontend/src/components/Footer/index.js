import styles from './index.module.css';

const Footer = () => {
    return (
        <footer id="footer">
        <div className={styles.navFooter}>
            <div className={styles.footerCol}>
                <h4>О нас</h4>
            </div>
            <div className={styles.footerCol}>
                <h4>Документация</h4>
                <div className={styles.socialLinks}>
                    <a className={styles.link} href="https://vk.com/pies_descalzos">ВК</a>
                    <a className={styles.link} href="https://github.com/LosPiesDescalzos">Git</a>
                </div>
            </div>
            <div className={styles.footerCol}>
                <h4>Что-то еще</h4>
            </div>
        </div>
    </footer>
    )
}
export default Footer;