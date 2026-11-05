import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  image: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Легкость в использовании',
    image: require('@site/static/img/easy.jpeg').default,
    description: (
      <>
        Не требует знаний в программировании для реализации базовых преобразований данных.

      </>
    ),
  },
  {
    title: 'Расширяемость',
    image: require('@site/static/img/extension.jpeg').default,
    description: (
      <>
        При необходимости можно расширить этап трансформации данных кодом написанный на Python.
      </>
    ),
  },
  {
    title: 'Основан на Open-Source решениях',
    image: require('@site/static/img/open_source.jpeg').default,
    description: (
      <>
        Ядро проекта создана на базе <a href="https://spark.apache.org/" target="_blank" rel="noopener">Apache Spark</a><br/>
        В примере используются дополнительные решения <a href="https://www.postgresql.org/" target="_blank" rel="noopener noreferrer">PostgreSQL</a>, <a href="https://superset.apache.org/" target="_blank" rel="noopener noreferrer">Apache Superset</a>, <a href="https://www.prisma.io/" target="_blank" rel="noopener noreferrer">Prisma</a>
      </>
    ),
  },
];

function Feature({title, image, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img src={image} className={styles.featureSvg} alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}