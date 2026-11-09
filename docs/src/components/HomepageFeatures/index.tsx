import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Translate, {translate} from '@docusaurus/Translate';

type FeatureItem = {
  title: string;
  image: string;
  link: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: translate({
      id: 'homepage.features.easyOfUse.title',
      message: 'Легкость в использовании',
    }),
    image: require('@site/static/img/easy.jpeg').default,
    link: 'docs/tutorial',
    description: (
      <Translate id="homepage.features.easyOfUse.description">
        Не требует знаний в программировании для реализации базовых преобразований данных.
      </Translate>
    ),
  },
  {
    title: translate({
      id: 'homepage.features.extensibility.title',
      message: 'Расширяемость',
    }),
    image: require('@site/static/img/extension.jpeg').default,
    link: 'docs/business_transformations',
    description: (
      <Translate id="homepage.features.extensibility.description">
        При необходимости можно расширить этап трансформации данных кодом написанный на Python.
      </Translate>
    ),
  },
  {
    title: translate({
      id: 'homepage.features.openSource.title',
      message: 'Основан на Open-Source решениях',
    }),
    image: require('@site/static/img/open_source.jpeg').default,
    link: 'https://opensource.org/',
    description: (
      <Translate
        id="homepage.features.openSource.description"
        values={{
          spark: (
            <a href="https://spark.apache.org/" target="_blank" rel="noopener">
              Apache Spark
            </a>
          ),
          postgresql: (
            <a href="https://www.postgresql.org/" target="_blank" rel="noopener noreferrer">
              PostgreSQL
            </a>
          ),
          superset: (
            <a href="https://superset.apache.org/" target="_blank" rel="noopener noreferrer">
              Apache Superset
            </a>
          ),
          prisma: (
            <a href="https://www.prisma.io/" target="_blank" rel="noopener noreferrer">
              Prisma
            </a>
          ),
        }}
      >
        {'Ядро проекта создана на базе {spark}\nВ примере используются дополнительные решения {postgresql}, {superset}, {prisma}'}
      </Translate>
    ),
  },
];

function Feature({title, image, link, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <a href={link}>
          <img src={image} className={styles.featureSvg} alt={title} />
        </a>
      </div>
      <div className="text--center padding-horiz--md">
        <a href={link}>
          <Heading as="h3">{title}</Heading>
        </a>
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