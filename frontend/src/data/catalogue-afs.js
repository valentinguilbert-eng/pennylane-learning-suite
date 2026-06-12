export const TARIFS = {
  session_1h: { label: "Session 1h", duree: "1h", visio: 200, presentiel: null, participants_max: 15, modules: "1 ou 2 modules" },
  session_2h: { label: "Session 2h", duree: "2h", visio: 400, presentiel: null, participants_max: 15, modules: "3 à 4 modules" },
  demi_journee: { label: "½ Journée", duree: "3h30", visio: 600, presentiel: 1000, participants_max: 15, modules: "jusqu'à 5 modules" },
  journee: { label: "Journée complète", duree: "7h", visio: 1200, presentiel: 2000, participants_max: 15, modules: "programme sur mesure" },
  journee_sur_mesure: { label: "Journée sur mesure (présentiel)", duree: "7h", visio: null, presentiel: 2000, participants_max: 15, modules: "100% personnalisé", note: "Frais de déplacement inclus pour 1 formateur, +300€ par formateur supplémentaire" },
}

export const THEMATIQUES = [
  {
    id: "comptabilite",
    emoji: "✏️",
    titre: "Saisie comptable / Révision / TVA / Paramétrage",
    modules: [
      {
        id: "saisie_comptable",
        titre: "Saisie comptable",
        description: "Maîtrisez la saisie sur Pennylane et exploitez toutes les automatisations disponibles pour gagner en efficacité et simplifier votre quotidien.",
      },
      {
        id: "revision",
        titre: "Révision",
        description: "Apprenez à structurer et accélérer vos révisions et clôtures dans Pennylane : maîtrisez les étapes clés du processus et activez les automatisations pour réduire les délais et fiabiliser vos arrêtés de comptes.",
      },
      {
        id: "tva",
        titre: "TVA",
        description: "Approfondissez votre maîtrise du module TVA de Pennylane : paramétrage avancé, gestion des spécificités fiscales et télédéclaration optimisée.",
      },
      {
        id: "parametrage",
        titre: "Paramétrage",
        description: "Paramétrez convenablement votre espace cabinet, vos dossiers et ceux de vos clients : connectez les outils tiers, contrôlez les échéances fiscales en un clic, introduction à la gestion interne, et bien plus encore.",
      },
    ],
  },
  {
    id: "achats",
    emoji: "📦",
    titre: "Module Achats & Notes de Frais",
    modules: [
      {
        id: "module_achat",
        titre: "Module Achat",
        description: "Maîtrisez chaque étape du cycle d'achat dans Pennylane : réception, traitement et validation des factures fournisseurs jusqu'au paiement final.",
      },
      {
        id: "notes_de_frais",
        titre: "Gestion des Notes de Frais",
        description: "Simplifiez la gestion des notes de frais de vos clients de A à Z : traitement des dépenses classiques, calcul des frais kilométriques et suivi des remboursements.",
      },
      {
        id: "demandes_achats",
        titre: "Gestion des Demandes d'Achats",
        description: "Maîtrisez le module de demandes d'achat de Pennylane : suivez chaque demande en temps réel et assurez leur traçabilité complète en les rattachant aux factures.",
      },
      {
        id: "circuit_validation",
        titre: "Circuit de validation",
        description: "Apprenez à paramétrer des circuits d'approbation adaptés à chaque structure : définissez les niveaux de validation, encadrez les dépenses et protégez vos clients contre les risques de fraude.",
      },
    ],
  },
  {
    id: "facturation",
    emoji: "📋",
    titre: "Facturation & Réforme de la Facturation Électronique",
    modules: [
      {
        id: "reforme_rfe",
        titre: "Réforme RFE",
        description: "Appréhendez les enjeux et le fonctionnement de la RFE : maîtrisez les notions d'e-invoicing et d'e-reporting, et repartez avec des réponses claires aux questions les plus fréquentes.",
      },
      {
        id: "methode_facturation",
        titre: "Méthode de facturation",
        description: "Maîtrisez chaque étape de votre facturation : émission de factures courantes et d'acompte, gestion des abonnements récurrents et création de vos documents commerciaux.",
      },
      {
        id: "relancer_clients",
        titre: "Relancer ses clients",
        description: "Configurez le système de relances Pennylane pour suivre vos encaissements, automatiser vos relances et réduire significativement vos démarches et délais de recouvrement.",
      },
      {
        id: "integration_gestion_commerciale",
        titre: "Intégration pour faciliter la gestion commerciale",
        description: "Découvrez les intégrations natives de Pennylane et apprenez à les valoriser auprès de vos clients pour automatiser leurs processus.",
      },
    ],
  },
  {
    id: "analytique",
    emoji: "📊",
    titre: "Analytique, Trésorerie & Pilotage",
    modules: [
      {
        id: "famille_analytique",
        titre: "Famille Analytique",
        description: "Apprenez à exploiter les catégories analytiques de Pennylane pour classer vos opérations, affiner votre suivi et obtenir une vision précise de l'activité financière de vos clients.",
      },
      {
        id: "plans_tresorerie",
        titre: "Plans de Trésorerie",
        description: "Maîtrisez le fonctionnement du plan de trésorerie Pennylane : paramétrez-le efficacement, interprétez les données et optimisez-le pour offrir à vos clients une vision claire et anticipée.",
      },
      {
        id: "outils_analyse",
        titre: "Les autres outils d'analyse de Pennylane",
        description: "Découvrez les outils d'analyse disponibles dans Pennylane, comprenez leurs utilités et apprenez à les utiliser pour offrir à vos clients une vision claire et pertinente de leur performance financière.",
      },
      {
        id: "posture",
        titre: "Posture",
        description: "Développez votre aisance pour présenter et valoriser les fonctionnalités Pennylane auprès de vos clients : les bons arguments, le bon niveau de détail et le bon timing pour maximiser leur adoption.",
      },
    ],
  },
  {
    id: "compte_pro",
    emoji: "🏦",
    titre: "Compte Pro & Financement",
    modules: [
      {
        id: "presentation_partenaire",
        titre: "Présentation de notre partenaire",
        description: "Découvrez le partenariat Pennylane x Swan et exploitez la solution bancaire intégrée, sans frais supplémentaire, qui enrichit votre offre.",
      },
      {
        id: "gestion_compte_pro",
        titre: "Gestion du compte Pro",
        description: "Maîtrisez l'intégralité des fonctionnalités du Compte Pro de Pennylane : règlement des factures, gestion des cartes bancaires, virements et suivi des encaissements clients.",
      },
      {
        id: "solutions_paiement",
        titre: "Solutions de paiement et financements",
        description: "Prélèvements, encaissements de chèques, TPE… choisissez la méthode d'encaissement adéquate ! Explorez les possibilités d'avances de trésorerie pour financer le BFR.",
      },
      {
        id: "mettre_en_avant_compte_pro",
        titre: "Mettre en avant le Compte Pro",
        description: "Développez votre argumentaire autour du Compte Pro : positionnement, discours clé et bonnes pratiques pour convaincre vos clients et renforcer votre rôle de conseiller.",
      },
    ],
  },
  {
    id: "onboarding",
    emoji: "🎯",
    titre: "Workshop — Onboarding Client",
    modules: [
      {
        id: "webinaire_embarquement",
        titre: "Webinaire embarquement client",
        description: "Formation collective sous format webinaire pour présenter et rendre autonome vos clients sur l'outil.",
        format_special: "Webinaire collectif — sans limite d'apprenants",
      },
      {
        id: "construction_strategie",
        titre: "Construction d'une stratégie",
        description: "Workshop interactif : travaillez en groupe sur votre stratégie client, identifiez les opportunités, levez les freins et repartez avec une feuille de route claire.",
      },
      {
        id: "mise_en_situation",
        titre: "Mise en situation",
        description: "Affinez votre maîtrise des fonctionnalités clés de Pennylane et renforcez votre posture commerciale : les bons arguments, les bonnes réponses aux objections.",
      },
    ],
  },
]

export const WEBINAIRES_EMBARQUEMENT = [
  {
    id: "webinar_collectif_collab",
    titre: "Webinar collectif — Plan Collaboratif",
    duree: "45 min",
    prix: "Offert",
    apprenants: "Sans limite",
    contenu: ["Présentation de Pennylane", "Paramétrage de l'outil", "Découverte des modules facturation", "Imports de factures, réconciliation"],
  },
  {
    id: "webinar_collectif_compta",
    titre: "Webinar collectif — Plan Collaboratif + Comptabilité",
    duree: "90 min",
    prix: "Offert",
    apprenants: "Sans limite",
    contenu: ["Présentation de Pennylane", "Paramétrage de l'outil", "Découverte des modules comptables", "Imports de factures, réconciliation"],
  },
  {
    id: "webinar_privatif",
    titre: "Webinar privatif — Plan au choix",
    duree: "Sur mesure",
    prix: "Sur devis",
    apprenants: "Sans limite",
    contenu: ["Embarquement selon plan d'abonnement", "Présentation exclusive à votre cabinet", "Accès limité à vos clients", "Adaptation possible à votre demande"],
  },
]
