from extensions import db
from models import Chemical, Industry, FAQ, SiteSetting, CustomCategory


def seed_initial_data():
    """Populate tables with starter content only if they are empty."""

    # --- Site Settings ---
    if SiteSetting.query.count() == 0:
        settings = {
            "site_name": "GOS Chemicals",
            "site_tagline": "Specialty Chemicals Manufactured & Exported from India",
            "hero_headline": "Specialty Chemicals Manufactured in India",
            "hero_subheadline": "Castor Oil & Derivatives | Chlorinated Paraffin Wax | Bleaching Clay",
            "hero_intro": "GOS Chemicals is a specialty chemical manufacturer and exporter based in India. We produce and supply Castor Oil & Derivatives, Chlorinated Paraffin Wax, and Bleaching Clay — along with custom chemical manufacturing for industrial buyers worldwide.",
            "contact_email": "info@goschemicals.com",
            "contact_phone": "+91-XXXXXXXXXX",
            "contact_address": "India",
            "cta_primary_label": "Request a Quote",
            "cta_secondary_label": "Explore Products",
            "seo_title_home": "Specialty Chemical Manufacturer & Exporter from India | GOS Chemicals",
            "seo_description_home": "GOS Chemicals is a specialty chemical manufacturer and exporter from India, producing Castor Oil & Derivatives, Chlorinated Paraffin Wax and Bleaching Clay, with custom chemical manufacturing capabilities.",
            "why_source_title": "Why Source from GOS Chemicals",
            "why_source_items": (
                "Manufacturing Capability: We operate our own production facilities, giving us direct control over quality, capacity, and lead times.|"
                "Product Understanding: Our team has hands-on technical knowledge of every product we manufacture — we understand the chemistry, not just the commerce.|"
                "Specification-Based Supply: We work to your specifications. Whether you need a standard grade or a custom formulation, we match the product to your process requirements.|"
                "Documentation: We provide complete documentation including Certificate of Analysis (COA), Material Safety Data Sheet (MSDS), and any additional paperwork your compliance or import process requires.|"
                "Export Coordination: We handle export logistics, packaging standards, and regulatory documentation for international shipments.|"
                "Direct Communication: You deal directly with people who know the product and the process — no layers of brokers or agents in between."
            ),
        }
        for key, value in settings.items():
            db.session.add(SiteSetting(key=key, value=value))
        db.session.commit()

    # --- Chemicals (Core) ---
    if Chemical.query.count() == 0:
        chemicals = [
            Chemical(
                slug="castor-oil-derivatives",
                name="Castor Oil & Derivatives",
                category="Core",
                summary="A versatile natural oil with a unique chemical profile, used across industrial, pharmaceutical, and cosmetic applications.",
                description=(
                    "Castor Oil is a vegetable oil pressed from castor beans (Ricinus communis). It is distinguished by its high concentration "
                    "of ricinoleic acid (~90%), which gives it unique properties — high viscosity, excellent lubricity, and solubility in alcohol. "
                    "These characteristics make it valuable across a wide range of industrial and consumer applications.\n\n"
                    "GOS Chemicals manufactures and supplies Castor Oil in several grades and derivative forms, including First Special Grade (FSG) Castor Oil, "
                    "Commercial Grade Castor Oil, Hydrogenated Castor Oil (Castor Wax), Dehydrated Castor Oil (DCO), and 12-Hydroxystearic Acid (12-HSA). "
                    "Each grade is produced to meet specific industrial requirements and international specifications."
                ),
                specification="Grades available: FSG Castor Oil, Commercial Grade Castor Oil, Hydrogenated Castor Oil (Castor Wax), Dehydrated Castor Oil (DCO), 12-Hydroxystearic Acid (12-HSA). Detailed COA available on request.",
                applications="Lubricants & greases,Paints & coatings (alkyd resins via DCO),Cosmetics & personal care,Pharmaceuticals,Plasticizers & polymer additives,Surfactants & emulsifiers,Textile finishing,Biodiesel feedstock",
                packaging="Available in drums, flexi-tanks, ISO tanks, or as per buyer specification.",
                cta_label="Request Castor Oil Quote",
                seo_title="Castor Oil & Derivatives Manufacturer India | GOS Chemicals",
                seo_description="GOS Chemicals manufactures and exports Castor Oil and derivatives including FSG, DCO, Hydrogenated Castor Oil, and 12-HSA from India.",
                display_order=1,
                status="published",
            ),
            Chemical(
                slug="chlorinated-paraffin-wax",
                name="Chlorinated Paraffin Wax",
                category="Core",
                summary="A chlorinated hydrocarbon used as a secondary plasticizer, flame retardant, and extreme-pressure lubricant additive.",
                description=(
                    "Chlorinated Paraffin Wax (CPW) is produced by chlorinating normal paraffin wax or liquid paraffin to varying chlorine content levels. "
                    "The resulting product is a viscous liquid or solid, depending on the chain length and chlorine percentage. CPW is widely used as a "
                    "secondary plasticizer in PVC compounds, a flame retardant additive, and an extreme-pressure additive in metalworking fluids.\n\n"
                    "GOS Chemicals manufactures CPW in multiple grades — short-chain, medium-chain, and long-chain — with chlorine content ranging from "
                    "40% to 70%, tailored to specific industrial applications."
                ),
                specification="Chlorine content: 40%–70%. Available in short-chain, medium-chain, and long-chain grades. Detailed specifications and COA provided on request.",
                applications="PVC plasticizer (secondary),Flame retardant additive,Metalworking fluids (extreme-pressure additive),Rubber processing,Paints & coatings,Sealants & adhesives",
                packaging="Available in drums, IBCs, or bulk tanker loads.",
                cta_label="Request CPW Quote",
                seo_title="Chlorinated Paraffin Wax Manufacturer India | GOS Chemicals",
                seo_description="GOS Chemicals manufactures Chlorinated Paraffin Wax (CPW) in multiple grades with 40-70% chlorine content for PVC, flame retardant, and metalworking applications.",
                display_order=2,
                status="published",
            ),
            Chemical(
                slug="bleaching-clay",
                name="Bleaching Clay",
                category="Core",
                summary="Acid-activated bentonite clay used for decolorizing and purifying edible oils, mineral oils, and industrial fluids.",
                description=(
                    "Bleaching Clay (also known as Bleaching Earth or Fuller's Earth) is an acid-activated bentonite clay used primarily for "
                    "decolorizing and purifying vegetable oils, mineral oils, and various industrial fluids. The activation process increases the "
                    "clay's surface area and adsorption capacity, making it effective at removing color pigments, impurities, and trace metals.\n\n"
                    "GOS Chemicals produces Bleaching Clay in multiple activity grades suited to different oil types and refining conditions. "
                    "Our products are used in edible oil refining, mineral oil purification, and industrial waste treatment."
                ),
                specification="Multiple activity grades available. Performance varies by oil type and refining conditions. Technical data sheet and COA available on request.",
                applications="Edible oil refining (palm, soy, sunflower, etc.),Mineral oil purification,Industrial lubricant reclamation,Waste oil treatment,Sugar decolorization",
                packaging="Available in 25 kg bags, jumbo bags, or as per buyer specification.",
                cta_label="Request Bleaching Clay Quote",
                seo_title="Bleaching Clay (Bleaching Earth) Manufacturer India | GOS Chemicals",
                seo_description="GOS Chemicals manufactures acid-activated Bleaching Clay for edible oil refining, mineral oil purification, and industrial applications.",
                display_order=3,
                status="published",
            ),
        ]
        db.session.add_all(chemicals)
        db.session.commit()

    # --- Industries ---
    if Industry.query.count() == 0:
        industries = [
            Industry(name="Paints & Coatings", description="Alkyd resins, plasticizers, and additives for the paint and coatings industry.", display_order=1),
            Industry(name="Water Treatment", description="Chemicals for municipal and industrial water treatment processes.", display_order=2),
            Industry(name="Mining & Mineral Processing", description="Flotation agents, flocculants, and processing chemicals for mining operations.", display_order=3),
            Industry(name="Pulp & Paper", description="Specialty chemicals for pulp processing and paper manufacturing.", display_order=4),
            Industry(name="Sugar Processing", description="Decolorizing agents and processing aids for sugar refining.", display_order=5),
            Industry(name="Food, Pharmaceutical & Cosmetic Applications", description="Ingredients and excipients meeting food-grade, pharma-grade, and cosmetic-grade specifications.", display_order=6),
            Industry(name="Industrial & Specialty Chemical Applications", description="Custom chemical solutions for general industrial and specialty chemical requirements.", display_order=7),
        ]
        db.session.add_all(industries)
        db.session.commit()

    # --- FAQs ---
    if FAQ.query.count() == 0:
        faqs = [
            FAQ(
                question="What products does GOS Chemicals manufacture?",
                answer="GOS Chemicals manufactures three core product lines: Castor Oil & Derivatives (including FSG Castor Oil, Commercial Grade, Hydrogenated Castor Oil, DCO, and 12-HSA), Chlorinated Paraffin Wax (in short-chain, medium-chain, and long-chain grades with 40–70% chlorine content), and Bleaching Clay (acid-activated bentonite in multiple activity grades). We also undertake custom chemical manufacturing.",
                display_order=1,
            ),
            FAQ(
                question="Is GOS Chemicals a manufacturer or a trader?",
                answer="We are a manufacturer. We operate our own production facilities, which gives us direct control over product quality, production capacity, and lead times. We are not a trading company or broker.",
                display_order=2,
            ),
            FAQ(
                question="What Castor Oil grades and derivatives do you offer?",
                answer="We offer First Special Grade (FSG) Castor Oil, Commercial Grade Castor Oil, Hydrogenated Castor Oil (Castor Wax), Dehydrated Castor Oil (DCO), and 12-Hydroxystearic Acid (12-HSA). Each is manufactured to meet specific industrial specifications.",
                display_order=3,
            ),
            FAQ(
                question="What grades of Chlorinated Paraffin Wax are available?",
                answer="We manufacture CPW in short-chain, medium-chain, and long-chain grades, with chlorine content ranging from 40% to 70%. The grade is selected based on the buyer's specific application — whether for PVC plasticizing, flame retardancy, or metalworking.",
                display_order=4,
            ),
            FAQ(
                question="What is Bleaching Clay used for?",
                answer="Bleaching Clay (Bleaching Earth / Fuller's Earth) is used for decolorizing and purifying edible oils, mineral oils, and industrial fluids. We produce it in multiple activity grades suited to different oil types and refining conditions.",
                display_order=5,
            ),
            FAQ(
                question="Can GOS Chemicals manufacture custom chemicals?",
                answer="Yes. Beyond our core product lines, we have the capability and infrastructure to manufacture chemicals to your specification. This includes water-treatment chemicals, phosphonates, mining chemicals, paint chemicals, sugar-processing chemicals, pulp & paper chemicals, food/pharmaceutical/cosmetic ingredients, and other specialty chemical requirements. Contact us with your requirements for a detailed discussion.",
                display_order=6,
            ),
            FAQ(
                question="How do I request a quotation?",
                answer="Use the Request a Quote form on our website, or contact us directly by email. Please include the product name, required specification or grade, intended application, estimated quantity, preferred packaging, and delivery destination. This helps us provide an accurate and timely quotation.",
                display_order=7,
            ),
            FAQ(
                question="Does GOS Chemicals supply internationally?",
                answer="Yes. We export to buyers worldwide. We handle export logistics, packaging standards, and all regulatory documentation required for international shipments, including Certificate of Analysis (COA) and Material Safety Data Sheet (MSDS).",
                display_order=8,
            ),
        ]
        db.session.add_all(faqs)
        db.session.commit()

    # --- Custom Manufacturing Categories ---
    if CustomCategory.query.count() == 0:
        categories = [
            CustomCategory(name="Water-treatment chemicals", display_order=1),
            CustomCategory(name="Phosphonates", display_order=2),
            CustomCategory(name="Mining chemicals", display_order=3),
            CustomCategory(name="Paint chemicals", display_order=4),
            CustomCategory(name="Sugar-processing chemicals", display_order=5),
            CustomCategory(name="Pulp & paper chemicals", display_order=6),
            CustomCategory(name="Food/pharmaceutical/cosmetic ingredients", display_order=7),
            CustomCategory(name="Other specialty chemical requirements", display_order=8),
        ]
        db.session.add_all(categories)
        db.session.commit()
