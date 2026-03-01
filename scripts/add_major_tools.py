#!/usr/bin/env python3
"""Add missing major tools from top organizations"""

import json

NEW_TOOLS = [
    # ===========================================
    # DATA VISUALIZATION
    # ===========================================
    {"name": "Apache Superset", "description": "Modern data exploration and visualization platform", "url": "https://superset.apache.org/", "category": "Data Science", "popular": True},
    {"name": "Highcharts", "description": "Interactive JavaScript charting library for web and mobile", "url": "https://www.highcharts.com/", "category": "Data Science"},
    {"name": "Observable", "description": "Collaborative data visualization and analysis platform", "url": "https://observablehq.com/", "category": "Data Science"},
    {"name": "Domo", "description": "Cloud-based business intelligence and data visualization platform", "url": "https://www.domo.com/", "category": "Analytics"},
    {"name": "ThoughtSpot", "description": "AI-powered analytics and business intelligence platform", "url": "https://www.thoughtspot.com/", "category": "Analytics"},
    {"name": "Amazon QuickSight", "description": "AWS cloud-native business intelligence service", "url": "https://aws.amazon.com/quicksight/", "category": "Analytics"},
    {"name": "Google Data Studio", "description": "Free data visualization and reporting tool by Google", "url": "https://datastudio.google.com/", "category": "Analytics"},
    
    # ===========================================
    # MICROSOFT DATA & ANALYTICS
    # ===========================================
    {"name": "Microsoft Fabric", "description": "Unified analytics platform combining data engineering, science, and BI", "url": "https://www.microsoft.com/en-us/microsoft-fabric", "category": "Data Engineering", "popular": True},
    {"name": "Azure Synapse Analytics", "description": "Limitless analytics service for enterprise data warehousing and big data", "url": "https://azure.microsoft.com/en-us/products/synapse-analytics/", "category": "Data Engineering", "popular": True},
    {"name": "Azure Data Factory", "description": "Cloud-based ETL and data integration service", "url": "https://azure.microsoft.com/en-us/products/data-factory/", "category": "Data Engineering"},
    {"name": "Power Automate", "description": "Microsoft workflow automation and RPA platform", "url": "https://powerautomate.microsoft.com/", "category": "Low-Code"},
    {"name": "Power Apps", "description": "Microsoft low-code application development platform", "url": "https://powerapps.microsoft.com/", "category": "Low-Code"},
    {"name": "Dynamics 365", "description": "Microsoft cloud-based ERP and CRM applications", "url": "https://dynamics.microsoft.com/", "category": "Business"},
    
    # ===========================================
    # CLOUD DATA WAREHOUSES & ANALYTICS
    # ===========================================
    {"name": "Google BigQuery", "description": "Serverless, highly scalable enterprise data warehouse", "url": "https://cloud.google.com/bigquery", "category": "Database", "popular": True},
    {"name": "Amazon Redshift", "description": "Fast, scalable cloud data warehouse by AWS", "url": "https://aws.amazon.com/redshift/", "category": "Database", "popular": True},
    {"name": "Adobe Analytics", "description": "Enterprise analytics for customer intelligence", "url": "https://business.adobe.com/products/analytics/adobe-analytics.html", "category": "Analytics"},
    {"name": "Splunk", "description": "Platform for searching, monitoring, and analyzing machine data", "url": "https://www.splunk.com/", "category": "Monitoring", "popular": True},
    {"name": "AppDynamics", "description": "Application performance monitoring and IT operations analytics", "url": "https://www.appdynamics.com/", "category": "Monitoring"},
    {"name": "Dynatrace", "description": "Software intelligence platform for cloud complexity", "url": "https://www.dynatrace.com/", "category": "Monitoring"},
    {"name": "Sumo Logic", "description": "Cloud-native machine data analytics platform", "url": "https://www.sumologic.com/", "category": "Monitoring"},
    
    # ===========================================
    # DATA PIPELINE & STREAMING
    # ===========================================
    {"name": "Logstash", "description": "Server-side data processing pipeline for Elastic Stack", "url": "https://www.elastic.co/logstash", "category": "Data Engineering"},
    {"name": "Fluentd", "description": "Open source data collector for unified logging layer", "url": "https://www.fluentd.org/", "category": "Data Engineering"},
    {"name": "Apache Pinot", "description": "Real-time distributed OLAP datastore for user-facing analytics", "url": "https://pinot.apache.org/", "category": "Database"},
    {"name": "Presto", "description": "Distributed SQL query engine for big data", "url": "https://prestodb.io/", "category": "Database"},
    {"name": "Trino", "description": "Fast distributed SQL query engine (formerly PrestoSQL)", "url": "https://trino.io/", "category": "Database"},
    {"name": "Amazon Athena", "description": "Interactive query service for S3 using SQL", "url": "https://aws.amazon.com/athena/", "category": "Database"},
    {"name": "Starburst", "description": "Enterprise analytics platform built on Trino", "url": "https://www.starburst.io/", "category": "Data Engineering"},
    
    # ===========================================
    # AWS SERVICES
    # ===========================================
    {"name": "Amazon S3", "description": "Scalable object storage service by AWS", "url": "https://aws.amazon.com/s3/", "category": "Storage", "popular": True},
    {"name": "Amazon EC2", "description": "Scalable virtual servers in the cloud", "url": "https://aws.amazon.com/ec2/", "category": "Cloud", "popular": True},
    {"name": "Amazon RDS", "description": "Managed relational database service by AWS", "url": "https://aws.amazon.com/rds/", "category": "Database", "popular": True},
    {"name": "Amazon DynamoDB", "description": "Fast, flexible NoSQL database service by AWS", "url": "https://aws.amazon.com/dynamodb/", "category": "Database", "popular": True},
    {"name": "Amazon SQS", "description": "Fully managed message queuing service", "url": "https://aws.amazon.com/sqs/", "category": "Message Queue"},
    {"name": "Amazon SNS", "description": "Pub/sub messaging and mobile notifications service", "url": "https://aws.amazon.com/sns/", "category": "Message Queue"},
    {"name": "Amazon CloudFront", "description": "Fast content delivery network (CDN) service", "url": "https://aws.amazon.com/cloudfront/", "category": "CDN"},
    {"name": "Amazon Route 53", "description": "Scalable DNS and domain name registration", "url": "https://aws.amazon.com/route53/", "category": "DevOps"},
    {"name": "Amazon ECS", "description": "Highly scalable container orchestration service", "url": "https://aws.amazon.com/ecs/", "category": "Container"},
    {"name": "Amazon EKS", "description": "Managed Kubernetes service by AWS", "url": "https://aws.amazon.com/eks/", "category": "Container"},
    {"name": "Amazon SageMaker", "description": "Build, train, and deploy ML models at scale", "url": "https://aws.amazon.com/sagemaker/", "category": "AI/ML", "popular": True},
    {"name": "Amazon Bedrock", "description": "Build generative AI applications with foundation models", "url": "https://aws.amazon.com/bedrock/", "category": "AI/ML"},
    
    # ===========================================
    # GCP SERVICES
    # ===========================================
    {"name": "Google Cloud Run", "description": "Fully managed serverless container platform", "url": "https://cloud.google.com/run", "category": "Serverless"},
    {"name": "Google Cloud Functions", "description": "Event-driven serverless compute platform", "url": "https://cloud.google.com/functions", "category": "Serverless"},
    {"name": "Google Firestore", "description": "Flexible, scalable NoSQL cloud database", "url": "https://firebase.google.com/products/firestore", "category": "Database"},
    {"name": "Google Vertex AI", "description": "Unified ML platform for building and deploying models", "url": "https://cloud.google.com/vertex-ai", "category": "AI/ML"},
    
    # ===========================================
    # ENTERPRISE & BUSINESS
    # ===========================================
    {"name": "HubSpot", "description": "CRM platform for marketing, sales, and customer service", "url": "https://www.hubspot.com/", "category": "Business", "popular": True},
    {"name": "Zendesk", "description": "Customer service and engagement platform", "url": "https://www.zendesk.com/", "category": "Business", "popular": True},
    {"name": "Intercom", "description": "Customer messaging platform for sales and support", "url": "https://www.intercom.com/", "category": "Business"},
    {"name": "Freshdesk", "description": "Cloud-based customer support software", "url": "https://www.freshworks.com/freshdesk/", "category": "Business"},
    {"name": "ServiceNow", "description": "Enterprise cloud platform for digital workflows", "url": "https://www.servicenow.com/", "category": "Business", "popular": True},
    {"name": "Workday", "description": "Enterprise cloud applications for finance and HR", "url": "https://www.workday.com/", "category": "Business"},
    {"name": "QuickBooks", "description": "Accounting software for small businesses", "url": "https://quickbooks.intuit.com/", "category": "Business"},
    {"name": "Xero", "description": "Cloud-based accounting software platform", "url": "https://www.xero.com/", "category": "Business"},
    
    # ===========================================
    # E-COMMERCE
    # ===========================================
    {"name": "Shopify", "description": "E-commerce platform for online stores", "url": "https://www.shopify.com/", "category": "Business", "popular": True},
    {"name": "WooCommerce", "description": "Open-source e-commerce plugin for WordPress", "url": "https://woocommerce.com/", "category": "Business"},
    {"name": "BigCommerce", "description": "E-commerce platform for growing businesses", "url": "https://www.bigcommerce.com/", "category": "Business"},
    
    # ===========================================
    # COMMUNICATION & REAL-TIME
    # ===========================================
    {"name": "Twilio", "description": "Cloud communications platform for SMS, voice, and video", "url": "https://www.twilio.com/", "category": "API", "popular": True},
    {"name": "Pusher", "description": "Real-time messaging APIs for web and mobile apps", "url": "https://pusher.com/", "category": "API"},
    {"name": "Ably", "description": "Realtime messaging infrastructure platform", "url": "https://ably.com/", "category": "API"},
    {"name": "PubNub", "description": "Real-time communication platform for chat and IoT", "url": "https://www.pubnub.com/", "category": "API"},
    {"name": "LiveKit", "description": "Open source WebRTC infrastructure for video/audio", "url": "https://livekit.io/", "category": "API"},
    {"name": "100ms", "description": "Video conferencing infrastructure for developers", "url": "https://www.100ms.live/", "category": "API"},
    {"name": "Webex", "description": "Cisco video conferencing and collaboration platform", "url": "https://www.webex.com/", "category": "Collaboration"},
    {"name": "Google Meet", "description": "Video conferencing service by Google", "url": "https://meet.google.com/", "category": "Collaboration"},
    
    # ===========================================
    # PRODUCTIVITY & NOTE-TAKING
    # ===========================================
    {"name": "Todoist", "description": "Task management and to-do list app", "url": "https://todoist.com/", "category": "Collaboration"},
    {"name": "Evernote", "description": "Note-taking and organization app", "url": "https://evernote.com/", "category": "Collaboration"},
    {"name": "Roam Research", "description": "Note-taking tool for networked thought", "url": "https://roamresearch.com/", "category": "Collaboration"},
    {"name": "Logseq", "description": "Privacy-first, open-source knowledge base", "url": "https://logseq.com/", "category": "Collaboration"},
    {"name": "Abstract", "description": "Version control and collaboration for designers", "url": "https://www.abstract.com/", "category": "Design"},
    
    # ===========================================
    # CLOUD STORAGE
    # ===========================================
    {"name": "Dropbox", "description": "Cloud storage and file synchronization service", "url": "https://www.dropbox.com/", "category": "Storage", "popular": True},
    {"name": "OneDrive", "description": "Microsoft cloud storage and file hosting service", "url": "https://www.microsoft.com/en-us/microsoft-365/onedrive/online-cloud-storage", "category": "Storage"},
    {"name": "Google Drive", "description": "Cloud storage and file backup by Google", "url": "https://www.google.com/drive/", "category": "Storage", "popular": True},
    {"name": "iCloud", "description": "Apple cloud storage and computing service", "url": "https://www.icloud.com/", "category": "Storage"},
    
    # ===========================================
    # MICROSOFT OFFICE
    # ===========================================
    {"name": "PowerPoint", "description": "Microsoft presentation software", "url": "https://www.microsoft.com/en-us/microsoft-365/powerpoint", "category": "Tool"},
    {"name": "Outlook", "description": "Microsoft email and calendar application", "url": "https://www.microsoft.com/en-us/microsoft-365/outlook/email-and-calendar-software-microsoft-outlook", "category": "Email"},
    {"name": "OneNote", "description": "Microsoft digital note-taking application", "url": "https://www.microsoft.com/en-us/microsoft-365/onenote/digital-note-taking-app", "category": "Collaboration"},
    {"name": "Microsoft Access", "description": "Microsoft database management system", "url": "https://www.microsoft.com/en-us/microsoft-365/access", "category": "Database"},
    {"name": "Microsoft Publisher", "description": "Desktop publishing application by Microsoft", "url": "https://www.microsoft.com/en-us/microsoft-365/publisher", "category": "Design"},
    {"name": "Yammer", "description": "Enterprise social networking service by Microsoft", "url": "https://www.microsoft.com/en-us/microsoft-365/yammer/yammer-overview", "category": "Collaboration"},
    {"name": "LinkedIn", "description": "Professional networking and career platform", "url": "https://www.linkedin.com/", "category": "Business", "popular": True},
    
    # ===========================================
    # AI CODING ASSISTANTS
    # ===========================================
    {"name": "GitHub Copilot", "description": "AI pair programmer by GitHub and OpenAI", "url": "https://github.com/features/copilot", "category": "AI/ML", "popular": True},
    {"name": "Tabnine", "description": "AI code completion assistant", "url": "https://www.tabnine.com/", "category": "AI/ML"},
    {"name": "Codeium", "description": "Free AI-powered code completion tool", "url": "https://codeium.com/", "category": "AI/ML"},
    {"name": "CodePen", "description": "Online code editor and front-end playground", "url": "https://codepen.io/", "category": "IDE/Editor"},
    
    # ===========================================
    # ADOBE CREATIVE SUITE
    # ===========================================
    {"name": "Adobe Photoshop", "description": "Industry-standard image editing and design software", "url": "https://www.adobe.com/products/photoshop.html", "category": "Design", "popular": True},
    {"name": "Adobe Illustrator", "description": "Vector graphics editor and design software", "url": "https://www.adobe.com/products/illustrator.html", "category": "Design", "popular": True},
    {"name": "Adobe Premiere Pro", "description": "Professional video editing software", "url": "https://www.adobe.com/products/premiere.html", "category": "Design"},
    {"name": "Adobe After Effects", "description": "Motion graphics and visual effects software", "url": "https://www.adobe.com/products/aftereffects.html", "category": "Design"},
    {"name": "Adobe Lightroom", "description": "Photo editing and management software", "url": "https://www.adobe.com/products/photoshop-lightroom.html", "category": "Design"},
    {"name": "Adobe InDesign", "description": "Desktop publishing and page layout software", "url": "https://www.adobe.com/products/indesign.html", "category": "Design"},
    {"name": "Adobe Acrobat", "description": "PDF creation and editing software", "url": "https://www.adobe.com/acrobat.html", "category": "Tool"},
    
    # ===========================================
    # 3D & GAME DEV
    # ===========================================
    {"name": "Blender", "description": "Free and open-source 3D creation suite", "url": "https://www.blender.org/", "category": "Design", "popular": True},
    {"name": "Cinema 4D", "description": "Professional 3D modeling and animation software", "url": "https://www.maxon.net/en/cinema-4d", "category": "Design"},
    {"name": "Houdini", "description": "3D animation and VFX software for film and games", "url": "https://www.sidefx.com/", "category": "Design"},
    {"name": "Substance 3D", "description": "Adobe 3D texturing and material creation tools", "url": "https://www.adobe.com/products/substance3d.html", "category": "Design"},
    {"name": "ZBrush", "description": "Digital sculpting tool for 3D artists", "url": "https://www.maxon.net/en/zbrush", "category": "Design"},
    {"name": "Cocos2d", "description": "Open-source game development framework", "url": "https://www.cocos.com/en/cocos2d-x", "category": "Game Engine"},
    {"name": "Phaser", "description": "Fast, free, fun HTML5 game framework", "url": "https://phaser.io/", "category": "Game Engine"},
    
    # ===========================================
    # SECURITY TOOLS
    # ===========================================
    {"name": "Metasploit", "description": "Penetration testing framework", "url": "https://www.metasploit.com/", "category": "Security"},
    {"name": "Kali Linux", "description": "Debian-based Linux distribution for security testing", "url": "https://www.kali.org/", "category": "Operating System"},
    {"name": "Parrot OS", "description": "Security-focused GNU/Linux distribution", "url": "https://www.parrotsec.org/", "category": "Operating System"},
    {"name": "Charles Proxy", "description": "HTTP proxy for debugging web traffic", "url": "https://www.charlesproxy.com/", "category": "Debugging"},
    {"name": "Fiddler", "description": "Web debugging proxy for any platform", "url": "https://www.telerik.com/fiddler", "category": "Debugging"},
    {"name": "Paw", "description": "Advanced API testing tool for Mac", "url": "https://paw.cloud/", "category": "API"},
]

def main():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    existing = {i.get('name', '').lower() for i in data}
    added = []
    skipped = []
    
    for tool in NEW_TOOLS:
        if tool['name'].lower() not in existing:
            data.append(tool)
            added.append(tool['name'])
        else:
            skipped.append(tool['name'])
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Added {len(added)} tools:")
    for name in added:
        print(f"  + {name}")
    
    if skipped:
        print(f"\nSkipped {len(skipped)} (already exist):")
        for name in skipped[:20]:
            print(f"  - {name}")
        if len(skipped) > 20:
            print(f"  ... and {len(skipped) - 20} more")
    
    print(f"\nTotal items now: {len(data)}")

if __name__ == '__main__':
    main()
