#coding:utf-8
import numpy as np
from helper.text_proposal_connector import TextProposalConnector
from helper.image import rotate_nms,nms,get_boxes



def normalize(data):
    if data.shape[0]==0:
        return data
    max_=data.max()
    min_=data.min()
    return (data-min_)/(max_-min_) if max_-min_!=0 else data-min_


class TextDetector:
    """
        Detect text from an image
    """
    def __init__(self,MAX_HORIZONTAL_GAP=30,MIN_V_OVERLAPS=0.6,MIN_SIZE_SIM=0.6):
        """
        pass
        """
        
        self.text_proposal_connector=TextProposalConnector(MAX_HORIZONTAL_GAP,MIN_V_OVERLAPS,MIN_SIZE_SIM)
        
    def detect(self, text_proposals,scores,size,
               TEXT_PROPOSALS_MIN_SCORE=0.7,
               TEXT_PROPOSALS_NMS_THRESH=0.3,
               TEXT_LINE_NMS_THRESH = 0.3,
               TEXT_LINE_SCORE=0.7
               ):
        ind = scores>TEXT_PROPOSALS_MIN_SCORE
        text_proposals = text_proposals[ind]
        scores = scores[ind]
        
        text_proposals, scores = nms(text_proposals,scores,TEXT_PROPOSALS_MIN_SCORE,TEXT_PROPOSALS_NMS_THRESH)
        if len(text_proposals)>0:
            scores                 = normalize(scores)
            text_lines,scores      = self.text_proposal_connector.get_text_lines(text_proposals, scores, size)##cluster lines
            text_lines             = get_boxes(text_lines)
            #text_lines, scores     = rotate_nms(text_lines,scores,TEXT_LINE_SCORE,TEXT_LINE_NMS_THRESH)##?cv2.dnn.rotate_nms error
            return text_lines, scores 
        else:
            return [],[]
        
