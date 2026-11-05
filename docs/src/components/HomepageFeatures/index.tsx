import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Легкость в использовании',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Не требует знаний в программировании для реализации базовых преобразований данных.

      </>
    ),
  },
  {
    title: 'Расширяемость',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        При необходимости можно расширить этап трансформации данных кодом написанный на Python.
      </>
    ),
  },
  {
    title: 'Основан на Open-Source решениях',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Ядро проекта создана на базе <a href="https://spark.apache.org/" target="_blank" rel="noopener">Apache Spark</a><br/>
        В примере используются дополнительные решения <a href="https://www.postgresql.org/" target="_blank" rel="noopener noreferrer">PostgreSQL</a>, <a href="https://superset.apache.org/" target="_blank" rel="noopener noreferrer">Apache Superset</a>, <a href="https://www.prisma.io/" target="_blank" rel="noopener noreferrer">Prisma</a>
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
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
