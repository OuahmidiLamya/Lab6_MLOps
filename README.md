# Lab 6 : Déploiement K8s d’un système MLOps Churn

## Étape 1 : Préparer l’environnement Kubernetes

Pour préparer le déploiement du système MLOps, un cluster Kubernetes local a été démarré à l’aide de Minikube avec le driver Docker et une version spécifique de Kubernetes. Un namespace dédié *churn-mlops* a ensuite été créé afin d’isoler les ressources du lab. Le contexte courant a été configuré pour utiliser ce namespace par défaut, puis l’état de l’environnement a été vérifié en listant les namespaces et les pods, confirmant que le cluster est opérationnel et prêt pour les étapes de déploiement suivantes.
<img width="1919" height="667" alt="image" src="https://github.com/user-attachments/assets/f42eb2b3-6fea-4866-81f3-0c2d1ef1e1ea" />
<img width="1919" height="373" alt="image" src="https://github.com/user-attachments/assets/d37f2297-df2c-42e4-be1d-2653368bf2ec" />
<img width="1919" height="139" alt="image" src="https://github.com/user-attachments/assets/e9f10f8c-a6e7-4d63-bcc4-7962a27b0fec" />
<img width="1919" height="178" alt="image" src="https://github.com/user-attachments/assets/48d76a7c-55ce-43ec-9d81-b6b91caa2e9b" />
<img width="1919" height="212" alt="image" src="https://github.com/user-attachments/assets/1f1d74cb-1b49-43c4-8148-b624b1d526a0" />
<img width="1919" height="133" alt="image" src="https://github.com/user-attachments/assets/ffd6f855-ed7f-414d-a0ea-1cfab40d426f" />

## Étape 2 : Préparer l’image Docker de l’API churn
Initialisation de l’environnement applicatif en préparant l’image Docker de l’API churn à partir d’un environnement Python standardisé. La version Python 3.12 a été vérifiée puis utilisée pour créer un environnement virtuel dédié, garantissant la cohérence entre les phases d’entraînement et de prédiction. Les dépendances nécessaires au fonctionnement de l’API et du modèle (FastAPI, Uvicorn, scikit-learn, pandas, numpy, joblib, etc.) ont été explicitement définies dans le fichier requirements.txt, puis installées via pip. Cette étape assure la reproductibilité de l’exécution, la compatibilité des bibliothèques et la stabilité du futur conteneur Docker.
<img width="1919" height="1043" alt="image" src="https://github.com/user-attachments/assets/0f849dc3-af4d-4757-a6ad-35ca9ddda9ab" />


## Étape 3 : Créer le dossier des manifests Kubernetes

Un dossier dédié nommé **k8s** a été ajouté à la racine du projet afin de centraliser l’ensemble des fichiers de configuration Kubernetes. Ce répertoire est destiné à contenir les manifests nécessaires au déploiement de l’API churn. La présence du dossier a été confirmée par la vérification de l’arborescence du projet, assurant une organisation cohérente avec les autres composants.

<img width="1918" height="950" alt="image" src="https://github.com/user-attachments/assets/e65560bc-72b5-4885-bda5-9f1c55eeaa31" />


## Étape 4 : Construire l’image Docker (tag versionné)

Initialisation de la phase de conteneurisation par la construction d’une image Docker de l’API churn à partir du Dockerfile du projet. L’image a été générée avec un **tag versionné (v1)** afin d’assurer une traçabilité claire des versions et d’éviter l’utilisation du tag `latest`. Une fois la construction terminée, la présence de l’image a été vérifiée localement à l’aide de la commande listant les images Docker, confirmant que l’image `churn-api:v1` est bien disponible et prête à être utilisée pour le déploiement Kubernetes..
<img width="1919" height="1036" alt="image" src="https://github.com/user-attachments/assets/39f39646-0108-4628-ae91-94ae35a2e538" />
<img width="1918" height="150" alt="image" src="https://github.com/user-attachments/assets/1aaf72c0-8557-4cd2-ac0b-5d56047a7bae" />

## Étape 5 : Charger explicitement l’image dans Minikube

Cette étape a consisté à exporter l’image Docker versionnée de l’API churn sous forme d’archive, puis à la charger explicitement dans l’environnement Minikube. La disponibilité de l’image dans le cluster a ensuite été vérifiée à l’aide des commandes Minikube, confirmant que l’image `churn-api:v1` est bien accessible pour un futur déploiement Kubernetes.

<img width="1919" height="270" alt="image" src="https://github.com/user-attachments/assets/6b398768-64df-4d92-87e1-ad3cafcf8b25" />


## Étape 6 : Deployment Kubernetes pour l’API churn

Initialisation du déploiement Kubernetes de l’API churn par la création d’un manifeste Deployment décrivant l’application, le nombre de réplicas et l’image Docker versionnée à utiliser. Le manifeste a ensuite été appliqué au cluster Minikube, permettant le lancement des pods correspondants. Le bon déroulement du déploiement a été vérifié via le suivi du rollout et la consultation de l’état des pods, confirmant que l’API est correctement exécutée dans l’environnement Kubernetes.

<img width="1919" height="446" alt="image" src="https://github.com/user-attachments/assets/65e0c41f-0131-47a4-bf44-2f89a3834bf1" />

## Étape 7 : Exposer l’API via un Service NodePort

Exposition de l’API churn au sein du cluster Kubernetes via un Service de type NodePort, permettant de rendre l’application accessible depuis l’extérieur du cluster. Un service dédié a été créé et associé aux pods de l’API, avec un mapping entre le port interne du conteneur et un port exposé sur le nœud. L’accès a ensuite été validé par un port-forwarding et des tests fonctionnels via l’interface Swagger, confirmant la disponibilité des endpoints `/health` et `/predict` ainsi que l’utilisation correcte du modèle actif.

<img width="1919" height="827" alt="image" src="https://github.com/user-attachments/assets/30a1139a-4e80-4358-b1dc-b7f9785b4e59" />
<img width="1919" height="291" alt="image" src="https://github.com/user-attachments/assets/8ef5ba0b-36b6-4116-b476-6b4a2c894edc" />
<img width="956" height="826" alt="image" src="https://github.com/user-attachments/assets/3c3c56d2-47a6-404b-9c1b-a17afa46c83e" />
<img width="1077" height="495" alt="image" src="https://github.com/user-attachments/assets/391a0d66-71e8-4a7f-80fb-62cdb35d21c0" />
<img width="948" height="798" alt="image" src="https://github.com/user-attachments/assets/14e86e39-d341-45f8-a944-0435bf1b3400" />


## Étape 8 : Injecter la configuration MLOps via ConfigMap

Cette étape a consisté à définir une configuration externe à l’application en créant un ConfigMap Kubernetes contenant les variables liées au modèle et au niveau de journalisation. Le ConfigMap a été appliqué au cluster puis injecté dans les pods de l’API via des variables d’environnement déclarées dans le manifest de déploiement. Le redémarrage contrôlé du déploiement a permis de propager la nouvelle configuration, et la vérification directe à l’intérieur des pods a confirmé la bonne prise en compte des valeurs définies.

<img width="1919" height="946" alt="image" src="https://github.com/user-attachments/assets/3f4886da-7ec4-4d3b-a5a0-cda09293dd0c" />
<img width="1919" height="551" alt="image" src="https://github.com/user-attachments/assets/46339762-8378-4537-a86c-bafe0a63972c" />


## Étape 9 : Gérer les secrets (MONITORING_TOKEN)

**Sécurisation** des informations sensibles a été réalisée en créant un *Secret Kubernetes* dédié au jeton de monitoring. La valeur du token a d’abord été encodée en base64, puis stockée dans un manifeste `secret.yaml` appliqué au cluster. Ce secret a ensuite été injecté comme variable d’environnement dans le déploiement de l’API via une référence sécurisée, suivie d’un redéploiement contrôlé des Pods. La bonne prise en compte a été validée en vérifiant la présence de la variable d’environnement directement à l’intérieur d’un Pod, sans exposer la valeur en clair.
<img width="1918" height="776" alt="image" src="https://github.com/user-attachments/assets/bd072478-9094-44f9-807a-00d611c5bdaa" />

<img width="1919" height="479" alt="image" src="https://github.com/user-attachments/assets/d455ce62-b1c5-4b12-9037-ff81ab213e50" />

## Étape 10 : Mise en place des endpoints de santé et des probes Kubernetes pour l’API Churn

**Mise en place** des mécanismes de supervision a consisté à enrichir l’API FastAPI avec des endpoints dédiés à la santé et à l’état de l’application, destinés à être utilisés par les probes Kubernetes. Les routes `/health`, `/startup` et `/ready` ont été ajoutées afin de vérifier respectivement l’état général de l’API, la disponibilité correcte du registry et du modèle au démarrage, ainsi que la capacité de l’application à recevoir du trafic. Après modification du code, l’image Docker a été reconstruite, exportée puis rechargée dans Minikube afin de prendre en compte ces changements et permettre à Kubernetes de superviser correctement le cycle de vie des Pods.

<img width="1919" height="879" alt="image" src="https://github.com/user-attachments/assets/b389b07a-a77a-4535-a04f-1ae08996be07" />


## Étape 11 : Ajouter les probes (liveness / readiness / startup)

Cette étape a consisté à configurer les mécanismes de surveillance de l’API Churn via les probes *liveness*, *readiness* et *startup*. Les endpoints `/health`, `/ready` et `/startup` ont été exploités par Kubernetes afin de vérifier respectivement la santé continue de l’application, sa disponibilité à recevoir du trafic et son bon démarrage (présence du registry et du modèle courant). Les probes ont été intégrées dans le manifeste `deployment.yaml`, puis le déploiement a été réappliqué et redémarré. Les vérifications ont confirmé que les Pods sont correctement redéployés, surveillés automatiquement et exposés au trafic uniquement lorsqu’ils sont prêts, garantissant ainsi la fiabilité et la résilience du service.
<img width="1919" height="752" alt="image" src="https://github.com/user-attachments/assets/a327ce43-1bba-46ff-81c8-700bc9284d2e" />
<img width="1919" height="458" alt="image" src="https://github.com/user-attachments/assets/0dec84b1-b1a6-4ef8-a6d9-b70c3d6d8b3d" />
<img width="1919" height="253" alt="image" src="https://github.com/user-attachments/assets/de484730-4cd0-4d9c-9bf2-724bee075964" />
<img width="1600" height="229" alt="image" src="https://github.com/user-attachments/assets/242b6dfe-ab29-487f-8dfc-dcaf08373438" />
<img width="1919" height="278" alt="image" src="https://github.com/user-attachments/assets/0862d1e4-48a7-488c-9bf7-2b33903b3327" />
<img width="1674" height="265" alt="image" src="https://github.com/user-attachments/assets/1b59f202-00cc-4a34-81c6-a870573a2726" />

## Étape 12 : Volume persistant pour registry + logs

Cette étape a consisté à mettre en place un volume persistant Kubernetes afin d’assurer la conservation des artefacts du modèle et des journaux applicatifs indépendamment du cycle de vie des Pods. Un *PersistentVolumeClaim* a été créé puis associé à un volume disponible du cluster. Un *Job* d’entraînement a ensuite été exécuté pour initialiser ce volume en générant un premier modèle et en écrivant les fichiers nécessaires dans le registry. Enfin, le volume a été monté dans le *Deployment* de l’API aux emplacements dédiés au registry, aux modèles et aux logs. Les vérifications ont confirmé que les Pods redémarrent correctement et que les données persistent bien entre les exécutions, garantissant la durabilité et la cohérence du système.
<img width="1919" height="667" alt="image" src="https://github.com/user-attachments/assets/3b622d24-48f1-4b45-b555-fcfa5701d80a" />
<img width="1919" height="522" alt="image" src="https://github.com/user-attachments/assets/def74e24-d3c7-4326-83e2-6b7cd264276b" />


## Étape 13 : NetworkPolicy

Sécurisation des communications internes du cluster par la mise en place d’une *NetworkPolicy* ciblant les Pods de l’API churn. Une règle d’ingress a été définie afin d’autoriser uniquement le trafic TCP entrant sur le port 8000 provenant des autres Pods du namespace, tout en bloquant les accès non explicitement autorisés. L’application de cette politique a permis de restreindre la surface d’exposition réseau de l’API et de vérifier son bon fonctionnement via les commandes de contrôle des NetworkPolicies actives.

<img width="1919" height="239" alt="image" src="https://github.com/user-attachments/assets/39c5ff62-c3f8-40a5-a7a6-762a8076dc72" />
<img width="1918" height="333" alt="image" src="https://github.com/user-attachments/assets/5746dff7-88a5-4cff-9c36-4f975512d380" />


## Étape 14 : Vérifications finales

Validation complète du déploiement via le contrôle de l’état des Pods et des Services Kubernetes, suivie de l’exposition locale de l’API par port-forwarding. Les endpoints `/health`, `/startup` et `/ready` sont testés avec succès depuis l’interface Swagger, confirmant la disponibilité, la préparation et la stabilité de l’application. Des requêtes `/predict` sont ensuite exécutées afin de vérifier le bon fonctionnement de l’inférence. Enfin, l’exécution du script de détection de dérive depuis un Pod confirme l’absence de drift sur les données récentes, attestant du bon état opérationnel du système MLOps déployé.
<img width="1918" height="303" alt="image" src="https://github.com/user-attachments/assets/e9cd6dfc-dd10-4aa0-9196-eaf45a0078a0" />
<img width="828" height="416" alt="image" src="https://github.com/user-attachments/assets/a658379b-649f-480b-a695-3415a6cf7f2a" />
<img width="844" height="796" alt="image" src="https://github.com/user-attachments/assets/48bdfbf8-2fbc-4840-bdeb-a1142ce46b8a" />
<img width="854" height="858" alt="image" src="https://github.com/user-attachments/assets/9bc84b5a-b4dd-41dc-82fe-8746ad165579" />
<img width="862" height="847" alt="image" src="https://github.com/user-attachments/assets/c7ccde89-f88e-4a8a-bc0d-71a337ceafd5" />
<img width="803" height="877" alt="image" src="https://github.com/user-attachments/assets/fc8a1407-a3ad-4e65-aba7-a18a325fc972" />
<img width="1919" height="228" alt="image" src="https://github.com/user-attachments/assets/2395566c-f338-48ec-8fdd-3a68749c5bce" />
<img width="1919" height="305" alt="image" src="https://github.com/user-attachments/assets/6a3e0328-f3d5-4476-95bf-65809fd446e5" />

