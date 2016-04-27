# -*- coding:utf-8 -*- 


from extensions import db


class CIRelation(db.Model):
    __tablename__ = "ci_relations"
    cr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_ci_id = db.Column(db.Integer,
                            db.ForeignKey("cis.ci_id"),
                            primary_key=True)
    second_ci_id = db.Column(db.Integer,
                             db.ForeignKey("cis.ci_id"),
                             primary_key=True)
    first_ci = db.relationship("CI",
                               primaryjoin="CI.ci_id==CIRelation.first_ci_id")
    second_ci = db.relationship(
        "CI", primaryjoin="CI.ci_id==CIRelation.second_ci_id")
    relation_type = db.Column(
        db.Enum("connect", "deploy", "install", "contain",
                name="relation_type"), nullable=False)
    more = db.Column(db.Integer, db.ForeignKey("cis.ci_id"))

    __table_args__ = (db.UniqueConstraint("first_ci_id", "second_ci_id",
                                          name="first_second_uniq"), )
